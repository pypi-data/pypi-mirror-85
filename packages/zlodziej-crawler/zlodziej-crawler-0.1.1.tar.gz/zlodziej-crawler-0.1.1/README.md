# zlodziej-crawler
![](docs/render.gif)

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Extending Project](#extending-project)

<!-- ABOUT THE PROJECT -->
## About The Project
Small web-scraper for scraping and processing offers from website [olx.pl](http://olx.pl).

### Built With
* [Poetry](https://github.com/python-poetry/poetry)
* [Pydantic](https://github.com/samuelcolvin/pydantic)
* [bs4](https://pypi.org/project/beautifulsoup4/)


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

`Poetry` is used for managing project dependencies, you can install it by: 
```
pip install poetry
```

### Installation
* Clone the repo
```
git clone https://gitlab.com/mwozniak11121/zlodziej-crawler-public.git
```
* Spawn poetry shell
```sh
poetry shell
```
* Install dependencies and package
```sh
poetry install
```
&nbsp;  

Or if you want to install package through `pip`
```sh
pip install zlodziej-crawler
```

<!-- USAGE EXAMPLES -->
## Usage

The only script made available is `steal`, which prompts for `url` with offer's category, e.g.
`olx.pl/nieruchomosci/mieszkania/wynajem/wroclaw/`  
and then scraps, processes and saves found offers.
(Results are saved in dir: `cwd / results`)

Example output for `RentOffer` looks like this:
![](docs/rent_offer.png)

## Extending Project
Project is meant to be easily extendable by adding new Pydantic models to `zlodziej_crawler/models.py`.  
`BaseOffer` serves purpose as a generic offer for all types of offers that are not specificly processed.  
`RentOffer` and its parent class `BaseOffer` look like this:

```
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

```

Project can be simply extended by adding matching classes based on other categories at [olx.pl](http://olx.pl).  
Adding new OfferType needs:
   * Parsing functions in `zlodziej_crawler/olx/offers_extraction/NEW_OFFER.py`
   * Factory function in `OLXParserFactory` (`zlodziej_crawler/olx/parser_factory.py`)
   * Matching offer category url in `OLXParserFactory.get_parser` (`zlodziej_crawler/olx/parser_factory.py`)

Currently any information found by scraper in `titlebox-details` section and not yet processed is saved as `unused_data`.
![](docs/unused_data.png)