from typing import List

import requests


class OLXIterator:
    def __init__(self, category_url: str):
        self._category_url = category_url
        self._base_url = "https://www.olx.pl/{category_url}/?page={{page}}".format(
            category_url=self._category_url
        )
        self.first_page = self._base_url.rsplit("/", maxsplit=1)[0] + "/"

    def get_all_pages_urls(self) -> List[str]:
        self._validate_url()
        results = [self.first_page]
        current_page = 2
        while True:
            url = self._base_url.format(page=current_page)
            response = requests.head(url)
            current_page += 1
            if str(response.status_code).startswith("2"):
                results.append(url)
            else:
                break
        return results

    def _validate_url(self):
        response = requests.head(self.first_page)
        if str(response.status_code).startswith("4"):
            raise ValueError(f"Entered category_url {self._category_url} was not found")
