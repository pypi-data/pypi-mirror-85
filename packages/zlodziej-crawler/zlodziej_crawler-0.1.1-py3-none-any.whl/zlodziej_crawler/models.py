from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Union

from pydantic import (
    BaseModel,
    HttpUrl,
    validator,
    Extra,
    PositiveInt,
    PositiveFloat,
)


class Website(str, Enum):
    UNKNOWN = "unknown"
    OLX = "olx.pl"


class OfferType(str, Enum):
    UNKNOWN = "unknown"
    PRIVATE = "private"
    DEVELOPER = "developer"


class BuildingType(str, Enum):
    UNKNOWN = "unknown"
    BLOK = "blok"
    KAMIENICA = "kamienica"
    DOM_WOLNOSTAJACY = "dom_wolnostojacy"
    SZEREGOWIEC = "szeregowiec"
    APARTAMENTOWIEC = "apartamentowiec"
    LOFT = "loft"
    POZOSTALE = "pozostale"


class BaseOffer(BaseModel):
    url: HttpUrl
    offer_name: str
    description: str
    id: PositiveInt
    time_offer_added: datetime
    views: PositiveInt
    location: str
    price: Union[PositiveInt, str]
    website: Optional[Website] = None
    unused_data: Optional[Dict] = None

    class Config:
        extra = Extra.forbid


class RentOffer(BaseOffer):
    rent: PositiveInt
    area: float

    number_of_rooms: Optional[str] = None
    offer_type: Optional[OfferType] = OfferType.UNKNOWN
    floor: Optional[str] = None
    building_type: Optional[BuildingType] = BuildingType.UNKNOWN
    furnished: Optional[bool] = None

    total_price: Optional[int] = None
    price_per_m: Optional[PositiveFloat] = None
    total_price_per_m: Optional[PositiveFloat] = None

    @validator("total_price", always=True)
    def calculate_total_price(cls, v, values):
        return values["price"] + values["rent"]

    @validator("price_per_m", always=True)
    def calculate_price_per_m(cls, v, values):
        try:
            return round(values["price"] / values["area"], 2)
        except ZeroDivisionError:
            return None

    @validator("total_price_per_m", always=True)
    def calculate_total_price_per_m(cls, v, values):
        try:
            return round(values["total_price"] / values["area"], 2)
        except ZeroDivisionError:
            return None
