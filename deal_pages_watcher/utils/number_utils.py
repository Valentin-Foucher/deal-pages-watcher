import re


def strip_non_alphanumerical_characters(s: str) -> float:
    return float(re.sub(',', r'.', re.sub(r'[^0-9.,]', '', s)))
