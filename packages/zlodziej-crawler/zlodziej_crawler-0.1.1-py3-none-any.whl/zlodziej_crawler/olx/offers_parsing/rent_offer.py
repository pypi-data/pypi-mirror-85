import re

from zlodziej_crawler.models import BuildingType, OfferType
from zlodziej_crawler.olx.offers_parsing.base_offer import leave_only_digits
from zlodziej_crawler.utilities import translate_to_enum


def extract_offer_type(content: str) -> OfferType:
    if "prywat" in content.lower():
        return OfferType.PRIVATE
    elif "biur" in content.lower():
        return OfferType.DEVELOPER
    else:
        return OfferType.UNKNOWN


def extract_floor(content: str) -> str:
    return content.lower().strip()


def extract_furnished(content: str) -> bool:
    if content.upper() == "TAK":
        return True
    return False


def extract_building_type(content: str) -> BuildingType:
    try:
        return translate_to_enum(content, BuildingType)
    except ValueError:
        return BuildingType.UNKNOWN


def extract_area(content: str) -> str:
    PATTERN = r"\d{1,}(?:,|.)\d{0,2}"
    area = re.findall(PATTERN, content).pop()
    return area.replace(",", ".")


def extract_number_of_rooms(content: str) -> str:
    return leave_only_digits(content)


def extract_rent(content: str) -> str:
    return leave_only_digits(content)


mapping = {
    "oferta od": (extract_offer_type, "offer_type"),
    "poziom": (extract_floor, "floor"),
    "umeblowane": (extract_furnished, "furnished"),
    "rodzaj zabudowy": (extract_building_type, "building_type"),
    "powierzchnia": (extract_area, "area"),
    "liczba pokoi": (extract_number_of_rooms, "number_of_rooms"),
    "czynsz (dodatkowo)": (extract_rent, "rent"),
}
