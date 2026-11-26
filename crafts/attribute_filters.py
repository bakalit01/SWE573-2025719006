"""Filter the catalogue by craft-specific attributes (US-19).

Once a single craft type is chosen, its active choice, multiple-choice, yes/no and number
fields become filters, e.g. "Dyes: Natural" for textiles or "Height between 10 and 30 cm"
for pottery. Text, long text, date and link fields are not filterable.

Matching is done in Python over the visible crafts of that one type (a small set), which
copes with values stored either as a single value or as a list, and with numbers stored as
text by older records.
"""

from decimal import Decimal, InvalidOperation

from .models import AttributeDefinition

T = AttributeDefinition.DataType
FILTERABLE = (T.CHOICE, T.MULTI_CHOICE, T.BOOLEAN, T.NUMBER)
YES_NO = {"yes": True, "no": False}


def _number(value):
    if isinstance(value, bool) or value in (None, ""):
        return None
    try:
        number = Decimal(str(value).strip())
    except InvalidOperation:
        return None
    return number if number.is_finite() else None


def _values(value):
    """A stored value as a list of strings (choice values may be single or a list)."""
    if value in (None, ""):
        return []
    items = value if isinstance(value, list) else [value]
    return [str(v) for v in items if v not in (None, "")]


def attribute_filters(craft_type, crafts, params):
    """Return (filters for the template, matching craft ids or None, chosen params).

    `crafts` are the crafts the viewer may see, already narrowed to `craft_type`.
    """
    definitions = craft_type.attributes.filter(is_active=True, data_type__in=FILTERABLE)
    rows = list(crafts.values_list("pk", "attributes"))
    specs, chosen, matching = [], {}, None

    def narrow(test):
        nonlocal matching
        ids = {pk for pk, attrs in rows if test((attrs or {}).get(d.key))}
        matching = ids if matching is None else matching & ids

    for d in definitions.order_by("order", "id"):
        param = f"a_{d.key}"
        spec = {"definition": d, "param": param}
        if d.data_type in (T.CHOICE, T.MULTI_CHOICE):
            used = {v for _, attrs in rows for v in _values((attrs or {}).get(d.key))}
            options = list(d.options) + sorted(used - set(d.options), key=str.casefold)
            if not used:
                continue  # nothing to filter on yet
            value = " ".join(params.get(param, "").split())
            spec.update(kind="choice", options=options, value=value)
            if value:
                chosen[param] = value
                wanted = value.casefold()
                narrow(lambda stored, w=wanted: any(v.casefold() == w for v in _values(stored)))
        elif d.data_type == T.BOOLEAN:
            value = params.get(param, "")
            spec.update(kind="boolean", value=value if value in YES_NO else "")
            if value in YES_NO:
                chosen[param] = value
                narrow(lambda stored, b=YES_NO[value]: stored is b)
        else:  # number
            low, high = _number(params.get(f"{param}_min")), _number(params.get(f"{param}_max"))
            spec.update(
                kind="number",
                min_value="" if low is None else f"{low.normalize():f}",
                max_value="" if high is None else f"{high.normalize():f}",
            )
            if low is not None:
                chosen[f"{param}_min"] = spec["min_value"]
            if high is not None:
                chosen[f"{param}_max"] = spec["max_value"]
            if low is not None or high is not None:

                def in_range(stored, low=low, high=high):
                    number = _number(stored)
                    return (
                        number is not None
                        and (low is None or number >= low)
                        and (high is None or number <= high)
                    )

                narrow(in_range)
        specs.append(spec)
    return specs, matching, chosen
