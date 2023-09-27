import re


def strip_non_alphanumerical_characters(s: str) -> float:
    return float(re.sub(',', r'.', re.sub(r'[^0-9.,]', '', s)))


def get_number_and_currency(s: str) -> dict[str, float | str]:
    return {'value': strip_non_alphanumerical_characters(s),
            'currency': re.sub(r'[^$€]', '', s)}
