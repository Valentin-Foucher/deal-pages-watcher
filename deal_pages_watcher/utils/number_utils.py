import re
import sys


def strip_non_alphanumerical_characters(s: str) -> float:
    try:
        return float(re.sub(',', r'.', re.sub(r'[^0-9.,]', '', s)))
    except ValueError:
        return float(sys.maxsize)


def get_number_and_currency(s: str) -> dict[str, float | str]:
    return {'value': strip_non_alphanumerical_characters(s),
            'currency': re.sub(r'[^$€]', '', s)}
