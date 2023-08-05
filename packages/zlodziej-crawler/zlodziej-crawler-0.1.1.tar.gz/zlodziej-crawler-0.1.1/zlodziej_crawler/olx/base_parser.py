from typing import List, Callable, Dict, Type

import bs4

from zlodziej_crawler.models import BaseOffer
from zlodziej_crawler.utilities import create_soup_from_url


class BaseParser:
    def __init__(
        self,
        offer_class: Type[BaseOffer],
        scrap_functions: List[Callable],
        parse_functions: Dict = None,
    ):
        self._offer_class = offer_class
        self._scrap_functions = scrap_functions
        self._parse_functions = parse_functions if parse_functions else {}

    def process_url(self, url: str, additional_data: Dict = None) -> BaseOffer:
        soup = create_soup_from_url(url, use_cache=True)
        scraped_data = self.scrap_data_from_soup(soup)

        scraped_data["url"] = url
        if additional_data:
            scraped_data.update(additional_data)

        return self.create_offer(scraped_data)

    def scrap_data_from_soup(self, soup: bs4.BeautifulSoup) -> Dict:
        result = dict()
        for function in self._scrap_functions:
            result.update(function(soup))

        return result

    def create_offer(self, scraped_data: Dict) -> BaseOffer:
        result = {}
        for key, params in self._parse_functions.items():
            function, new_key = params
            try:
                result[new_key] = function(scraped_data[key])
            except KeyError:
                continue
            except Exception as e:
                raise ValueError(
                    f"Exception {e} occured while\n executing function {function}\n on data {scraped_data[key]}\n on url {scraped_data['url']}"
                )
            del scraped_data[key]
        result["unused_data"] = scraped_data

        return self._offer_class.parse_obj(result)
