import math
import re
import sys
from typing import Optional
from urllib.error import HTTPError

from bs4 import BeautifulSoup, PageElement, ResultSet
import urllib.request

from deal_pages_watcher.utils.number_utils import get_number_and_currency, strip_non_alphanumerical_characters


def is_deal_correct(percent: float, first_price: int, second_price: int) -> bool:
    return \
        first_price != 0 and \
        second_price != 0 and (
                math.isclose(1 - first_price / second_price, percent / 100, abs_tol=0.0001) or
                math.isclose(1 - second_price / first_price, percent / 100, abs_tol=0.0001)
        )


def get_closest_ancestor_that_includes_h1(anchor: PageElement) \
        -> tuple[int, Optional[str], Optional[ResultSet[PageElement]], float]:
    max_ancestor_level = 0
    percent = strip_non_alphanumerical_characters(anchor.get_text())
    ancestor = anchor
    h1 = None
    product = None
    product_prices = None

    while ancestor := ancestor.parent:
        max_ancestor_level += 1

        prices = list(map(get_number_and_currency,
                          ancestor.find_all(string=re.compile(r'[\s\u00A0]*\d+([,.]\d+)?[\s\u00A0]*[€$][\s\u00A0]*'),
                                            limit=2)))

        h1 = ancestor.find('h1')
        if len(prices) == 2 and h1 is not None and is_deal_correct(percent, *[p['value'] for p in prices]):
            product_prices = prices
            break

    if h1:
        product = h1.get_text()
        h1_ancestor = h1
        while (h1_ancestor := h1_ancestor.parent) != ancestor:
            max_ancestor_level += 1

    return max_ancestor_level, product, product_prices, percent


def get_discount_details(url: str) -> dict[str, str | list[dict[str, float | str]] | int]:
    characteristics = {'product': None,
                       'prices': None,
                       'discount': None}

    try:
        webpage = urllib.request.urlopen(url)
    except HTTPError:
        return characteristics

    characteristics['level'] = sys.maxsize
    soup = BeautifulSoup(webpage, 'html.parser')

    if soup.find(string=re.compile(r'^([dD]escription.*|[Cc]aract.ristiques?|[Aa]jouter\sau\spanier)$')):

        for anchor in soup.find_all(
                string=re.compile(r'^[\s\u00A0]*-[\s\u00A0]*\d+([,.]\d+)?[\s\u00A0]*%[\s\u00A0]*$')
        ):
            if not (anchor.get_text()) or anchor.name == 'script':
                continue

            evaluated_minimum, product, prices, percent = get_closest_ancestor_that_includes_h1(anchor)
            if not prices:
                continue

            prices = sorted(prices, key=lambda p: p['value'])

            if characteristics['level'] > evaluated_minimum:
                characteristics = {
                    'level': evaluated_minimum,
                    'product': product,
                    'prices': prices,
                    'discount': percent
                }

    characteristics.pop('level')
    return characteristics
