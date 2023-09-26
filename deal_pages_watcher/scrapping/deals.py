import math
import re
import sys
from typing import Optional

from bs4 import BeautifulSoup, PageElement, ResultSet
import urllib.request

from deal_pages_watcher.utils.number_utils import strip_non_alphanumerical_characters

tests = ['https://www.kookai.fr/products/c4527-a8?variant=42363208630448',
         'https://www.zalando.fr/only-pullover-ecru-on321i1la-g11.html',
         'https://www.zalando.fr/k-way-le-vrai-claudette-veste-impermeable-black-pure-kw121g02d-q11.html']


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

        prices = list(map(strip_non_alphanumerical_characters,
                          ancestor.find_all(string=re.compile(r'^\s*\d+([,.]\d+)?\s*[€$]\s*$'), limit=2)))

        h1 = ancestor.find('h1')
        if len(prices) == 2 and h1 is not None and is_deal_correct(percent, *prices):
            product_prices = prices
            break

    if h1:
        product = h1.get_text()
        h1_ancestor = h1
        while (h1_ancestor := h1_ancestor.parent) != ancestor:
            max_ancestor_level += 1

    return max_ancestor_level, product, product_prices, percent


def get_discount_details(url: str) -> dict[str, str | float | int]:
    webpage = urllib.request.urlopen(url)
    soup = BeautifulSoup(webpage, 'html.parser')

    characteristics = {'level': sys.maxsize,
                       'product': None,
                       'prices': None,
                       'discount': None}

    if soup.find(string=re.compile(r'^([dD]escription|[Cc]aract.ristiques?|[Aa]jouter\sau\spanier)$')):

        for anchor in soup.find_all(string=re.compile(r'^\s*-\s*\d+([,.]\d+)?\s*%\s*$')):
            if not (anchor.get_text()) or anchor.name == 'script':
                continue

            evaluated_minimum, product, prices, percent = get_closest_ancestor_that_includes_h1(anchor)
            if not prices:
                continue

            if characteristics['level'] > evaluated_minimum:
                characteristics = {
                    'level': evaluated_minimum,
                    'product': product,
                    'prices': prices,
                    'discount': percent
                }

    characteristics.pop('level')
    return characteristics


print(get_discount_details("https://www.zalando.fr/rieker-mules-blau-ri111a0z2-k11.html"))
print(get_discount_details('https://www.auchan.fr/electromenager-cuisine/bonnes-affaires-electromenager-cuisine/ca-10608361#e5a33f79-2203-48e6-8136-3450f688e301_566'))
print(get_discount_details('https://www.auchan.fr/samsung-lave-linge-hublot-ww80ta046th-8-kg-1400-t-min/pr-C1331172'))
print(get_discount_details('https://www.kookai.fr/products/c4527-a8?variant=42363208630448'))
print(get_discount_details('https://www.zalando.fr/buffalo-aspha-bottines-a-lacets-silverblue-bu311n0ep-d11.html'))