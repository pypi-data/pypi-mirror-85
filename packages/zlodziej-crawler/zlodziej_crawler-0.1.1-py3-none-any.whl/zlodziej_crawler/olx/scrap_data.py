from typing import List, Dict

import bs4
from unidecode import unidecode


def _extract_offer_details(soup: bs4.BeautifulSoup) -> Dict:
    details = soup.find_all("ul", {"class": "offer-details"}).pop()
    tags = details.find_all("li", {"class": "offer-details__item"})

    results = dict()
    for tag in tags:
        key, value = _extract_tag(tag)
        results[key] = value.strip()

    offer_description = _extract_tag(details.find_next("div", {"id": "textContent"}))
    results["opis"] = " ".join(offer_description).strip()

    return results


def _extract_titlebox_details(soup: bs4.BeautifulSoup) -> Dict:
    titlebox = soup.find_all("div", {"class": "offer-titlebox"}).pop()

    offer_name = _extract_tag(titlebox.find_next("h1")).pop()
    try:
        price_label = _extract_tag(
            titlebox.find_next("div", {"class": "pricelabel"})
        ).pop(0)
    except IndexError:
        price_label = ""

    result = {"cena": unidecode(price_label), "nazwa oferty": unidecode(offer_name)}

    return result


def _extract_location(soup: bs4.BeautifulSoup) -> Dict:
    location_bar = soup.find_all("div", {"class": "offer-user__location"}).pop()
    location = _extract_tag(location_bar.find_next("address")).pop()
    result = {"lokacja": unidecode(location)}

    return result


def _extract_bottombar(soup: bs4.BeautifulSoup) -> Dict:
    bottom_bar = soup.find_all("div", {"id": "offerbottombar"}).pop()
    tags = [_extract_tag(tag) for tag in bottom_bar.find_all("li")]

    result = {
        "czas dodania": _concat_strings(tags[0]),
        "wyswietlenia": _concat_strings(tags[1]),
        "id ogloszenia": _concat_strings(tags[2]),
    }

    return result


def _concat_strings(contents: List[str]) -> str:
    return " ".join(contents).strip()


def _extract_tag(tag: bs4.Tag) -> List[str]:
    if not tag:
        return []
    return [_clean_up_field(field) for field in tag.get_text().split("\n") if field]


def _clean_up_field(value: str) -> str:
    return value.strip().lower()


functions_to_execute = [
    _extract_offer_details,
    _extract_titlebox_details,
    _extract_location,
    _extract_bottombar,
]
