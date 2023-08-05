import re
from typing import List

import bs4

from zlodziej_crawler.olx.iterator import OLXIterator
from zlodziej_crawler.utilities import create_soup_from_url


class OLXCrawler:
    def get_offers(self, category_url: str, page_limit: int = None) -> List[str]:
        iterator = OLXIterator(category_url=category_url)
        return self._get_offers_urls(
            pages=iterator.get_all_pages_urls(), page_limit=page_limit
        )

    def _get_offers_urls(self, pages: List[str], page_limit: int = None) -> List[str]:
        iter_pages = pages[:page_limit] if page_limit else pages

        offers = []
        for page in iter_pages:
            offers.extend(
                self._extract_urls(create_soup_from_url(page, use_cache=False))
            )

        cleaned_up_offers = [self._clean_up_url(url) for url in offers]

        return list(set(cleaned_up_offers))

    def _extract_urls(self, soup: bs4.BeautifulSoup) -> List[str]:
        table = soup.find_all("table", {"id": "offers_table"}).pop()
        offers = table.find_all("div", {"class": "offer-wrapper"})
        return list(set([self._extract_url(tag) for tag in offers]))

    @staticmethod
    def _extract_url(tag: bs4.Tag) -> str:
        return tag.find_next("h3").find_next("a").get("href")

    @staticmethod
    def _clean_up_url(url: str) -> str:
        PATTERN = r"(.*\.html).*"
        return re.findall(PATTERN, url).pop()
