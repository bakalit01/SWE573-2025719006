"""Measurement units used around the world, and conversions for display.

Makers record sizes in the units they use; the craft page shows the original value first
and a converted value (metric ↔ imperial) after it. Traditional or local measures that have
no fixed conversion (a hand span, a "karış", an "arşın") are kept as free text.
"""

from decimal import Decimal

LENGTH_UNITS = [
    ("mm", "millimetres (mm)"),
    ("cm", "centimetres (cm)"),
    ("m", "metres (m)"),
    ("in", "inches (in)"),
    ("ft", "feet (ft)"),
]
WEIGHT_UNITS = [
    ("g", "grams (g)"),
    ("kg", "kilograms (kg)"),
    ("oz", "ounces (oz)"),
    ("lb", "pounds (lb)"),
]

_TO_CM = {
    "mm": Decimal("0.1"),
    "cm": Decimal(1),
    "m": Decimal(100),
    "in": Decimal("2.54"),
    "ft": Decimal("30.48"),
}
_TO_G = {
    "g": Decimal(1),
    "kg": Decimal(1000),
    "oz": Decimal("28.349523"),
    "lb": Decimal("453.59237"),
}
METRIC_LENGTH = {"mm", "cm", "m"}
METRIC_WEIGHT = {"g", "kg"}


def fmt(value, places=2):
    """1.50 → '1.5', 24.00 → '24', 0.1234 → '0.12' (at most `places` decimals, no trailing 0s)."""
    if value is None:
        return ""
    q = Decimal(value).quantize(Decimal(1).scaleb(-places))
    return format(q.normalize(), "f")


def fmt_converted(value):
    """Converted values are approximate: 1 decimal, or whole numbers from 100 upwards."""
    return fmt(value, 0 if abs(Decimal(value)) >= 100 else 1)


def convert_length(value, unit, target):
    return Decimal(value) * _TO_CM[unit] / _TO_CM[target]


def convert_weight(value, unit, target):
    return Decimal(value) * _TO_G[unit] / _TO_G[target]


def describe_size(height, width, depth, unit):
    """('24 × 18 × 9 cm', 'H × W × D', '≈ 9.45 × 7.09 × 3.54 in') or None if no size."""
    parts = [(label, v) for label, v in (("H", height), ("W", width), ("D", depth)) if v]
    if not parts or not unit:
        return None
    original = " × ".join(fmt(v) for _, v in parts) + f" {unit}"
    axes = " × ".join(label for label, _ in parts)
    if unit in METRIC_LENGTH:
        target = "in"
    else:
        target = "cm"
    converted = "≈ " + " × ".join(fmt_converted(convert_length(v, unit, target)) for _, v in parts)
    return {"original": original, "axes": axes, "converted": f"{converted} {target}"}


def describe_weight(weight, unit):
    if not weight or not unit:
        return None
    if unit in METRIC_WEIGHT:
        target = "lb" if convert_weight(weight, unit, "g") >= 454 else "oz"
    else:
        target = "kg" if convert_weight(weight, unit, "g") >= 1000 else "g"
    return {
        "original": f"{fmt(weight)} {unit}",
        "converted": f"≈ {fmt_converted(convert_weight(weight, unit, target))} {target}",
    }
