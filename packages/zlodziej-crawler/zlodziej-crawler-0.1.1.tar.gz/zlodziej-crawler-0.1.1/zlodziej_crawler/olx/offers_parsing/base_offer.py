import re
from datetime import datetime

from dateutil.parser import parse

from zlodziej_crawler.models import Website
from zlodziej_crawler.utilities import (
    translate_months,
    translate_to_enum,
    translate_city,
)


def leave_only_digits(content: str) -> str:
    return re.sub(r"\D", "", content)


def extract_description(content: str) -> str:
    return content


def extract_price(content: str) -> str:
    return leave_only_digits(content)


def extract_offer_name(content: str) -> str:
    return content


def extract_location(content: str) -> str:
    return content


def extract_url(content: str) -> str:
    return content


def extract_city(content: str) -> str:
    return translate_city(content)


def extract_time_offer_added(content: str) -> datetime:
    PATTERN = r".*(\d\d:\d\d.*)"
    cleaned_up = re.findall(PATTERN, content).pop()

    words = cleaned_up.lstrip("o ").split(" ")
    translated = []
    for word in words:
        try:
            translated.append(translate_months(word))
        except KeyError:
            translated.append(word)
    return parse(" ".join(translated))


def extract_id(content: str) -> str:
    return leave_only_digits(content)


def extract_views(content: str) -> str:
    return leave_only_digits(content)


def extract_website(content: str) -> str:
    return translate_to_enum(content, Website)


mapping = {
    "opis": (extract_description, "description"),
    "cena": (extract_price, "price"),
    "nazwa oferty": (extract_offer_name, "offer_name"),
    "lokacja": (extract_location, "location"),
    "url": (extract_url, "url"),
    "czas dodania": (extract_time_offer_added, "time_offer_added"),
    "id ogloszenia": (extract_id, "id"),
    "wyswietlenia": (extract_views, "views"),
    "strona": (extract_website, "website"),
}
