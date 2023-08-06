from decimal import Decimal
from decimal import Context

def binary_decompose(value):
    values = set()
    binary_string = bin(value)[2:]
    length = len(binary_string) - 1
    for c in binary_string:
        if c == "1":
            values.add(2**length)
        length -= 1
    return values


def decimal_change_base(number, base=16, characters="0123456789abcdefghijklmnopqrstuvwxyz"):
    digits = []
    while number:
        digits.append( number % base )
        number //= base
    digits.reverse()
    if not digits:
        digits.append(0)
    if characters:
        return "".join([characters[x] for x in digits])
    else:
        return digits


def get_float_part(value, precision=7):
    value = abs(value - int(value))
    value *= 10 ** precision
    value = int(value)
    return value


def float_split(value, precision=7):
    if value >= 0:
        sign = 1
    else:
        sign = -1
    value = abs(value)
    int_value = int(value)
    float_value = get_float_part(value, precision)
    return sign, int_value, float_value


if hasattr(int, "from_bytes"):
    from_bytes = int.from_bytes
else:
    def from_bytes(value_bytes, byteorder="big"):
        t = 0
        if byteorder.lower() != "big":
            value_bytes = bytearray(value_bytes)
            value_bytes.reverse()
        else:
            value_bytes = bytearray(value_bytes)
        for x in value_bytes:
            t = t*256 + x
        return t


try:
    NUMERIC_TYPES = (int, long, float)
except NameError:
    NUMERIC_TYPES = (int, float)
