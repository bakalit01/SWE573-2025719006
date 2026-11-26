"""Helpers for controlled terms with alternate spellings (US-28).

Materials, techniques, communities and regions keep their other names or spellings in a
comma-separated `other_names` field. Search matches them, and a name typed in a form is
matched to the existing term it spells, so new duplicates aren't created.
"""


def split_names(text):
    return [n for n in (" ".join(part.split()) for part in (text or "").split(",")) if n]


def join_names(names, exclude=()):
    """Comma-separated, without repeats (ignoring capitals) or the excluded names."""
    seen = {n.casefold() for n in exclude}
    kept = []
    for name in names:
        if name.casefold() not in seen:
            seen.add(name.casefold())
            kept.append(name)
    return ", ".join(kept)


def find_term(model, name):
    """The term called `name`, or known by it as an alternate spelling; else None."""
    name = " ".join((name or "").split())
    if not name:
        return None
    term = model.objects.filter(name__iexact=name).first()
    if term:
        return term
    wanted = name.casefold()
    for term in model.objects.filter(other_names__icontains=name):
        if any(n.casefold() == wanted for n in split_names(term.other_names)):
            return term
    return None
