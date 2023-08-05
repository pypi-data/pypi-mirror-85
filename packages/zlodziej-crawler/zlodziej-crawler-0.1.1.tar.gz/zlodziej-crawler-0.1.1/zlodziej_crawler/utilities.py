from enum import Enum
from typing import Union

import bs4
import requests
from unidecode import unidecode

from zlodziej_crawler.cache_helper import cache_get


def translate_to_enum(value: Union[str, Enum], enum_class):
    enum_value = unidecode(value).lower().strip().replace(" ", "_")
    return enum_class(enum_value)


def translate_city(city: str) -> str:
    EXCEPTIONS = {"zielona gora": "zielonagora"}

    translated = unidecode(city).lower()
    try:
        return EXCEPTIONS[translated]
    except KeyError:
        return translated.replace(" ", "-")


def translate_months(content: str) -> str:
    mapping = {
        "styczen": "january",
        "stycznia": "january",
        "luty": "february",
        "lutego": "february",
        "marzec": "march",
        "marca": "march",
        "kwiecien": "april",
        "kwietnia": "april",
        "maj": "may",
        "maja": "may",
        "czerwiec": "june",
        "czerwca": "june",
        "lipiec": "july",
        "lipca": "july",
        "sierpien": "august",
        "sierpnia": "august",
        "wrzesien": "september",
        "wrzesnia": "september",
        "pazdziernik": "october",
        "pazdziernika": "october",
        "listopad": "november",
        "listopada": "november",
        "grudzien": "december",
        "grudnia": "december",
    }
    key = unidecode(content).lower().strip()
    return mapping[key]


def create_soup_from_url(url: str, use_cache: bool = True) -> bs4.BeautifulSoup:
    if use_cache:
        content = cache_get(url)
    else:
        content = requests.get(url).content

    return bs4.BeautifulSoup(content, "lxml")


def extract_category_url(url: str) -> str:
    try:
        category_url = url.split(".pl")[1]
    except IndexError:
        raise ValueError("Entered url isn't valid")

    category_url = category_url.split("?")[0]

    if category_url.startswith("/"):
        category_url = category_url[1:]
    if category_url.endswith("/"):
        category_url = category_url[:-1]

    return category_url.lower()
