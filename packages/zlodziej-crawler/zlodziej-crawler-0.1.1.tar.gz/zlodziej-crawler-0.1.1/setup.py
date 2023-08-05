# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zlodziej_crawler',
 'zlodziej_crawler.olx',
 'zlodziej_crawler.olx.offers_parsing',
 'zlodziej_crawler.tools']

package_data = \
{'': ['*']}

install_requires = \
['Pygments>=2.7.1,<3.0.0',
 'Unidecode>=1.1.1,<2.0.0',
 'bs4>=0.0.1,<0.0.2',
 'click>=7.1.2,<8.0.0',
 'lxml>=4.5.2,<5.0.0',
 'pydantic>=1.6.1,<2.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'requests>=2.24.0,<3.0.0',
 'tqdm>=4.50.2,<5.0.0']

entry_points = \
{'console_scripts': ['steal = zlodziej_crawler.olx.get_offers:main']}

setup_kwargs = {
    'name': 'zlodziej-crawler',
    'version': '0.1.1',
    'description': '',
    'long_description': "# zlodziej-crawler\n![](docs/render.gif)\n\n<!-- TABLE OF CONTENTS -->\n## Table of Contents\n\n* [About the Project](#about-the-project)\n  * [Built With](#built-with)\n* [Getting Started](#getting-started)\n  * [Prerequisites](#prerequisites)\n  * [Installation](#installation)\n* [Usage](#usage)\n* [Extending Project](#extending-project)\n\n<!-- ABOUT THE PROJECT -->\n## About The Project\nSmall web-scraper for scraping and processing offers from website [olx.pl](http://olx.pl).\n\n### Built With\n* [Poetry](https://github.com/python-poetry/poetry)\n* [Pydantic](https://github.com/samuelcolvin/pydantic)\n* [bs4](https://pypi.org/project/beautifulsoup4/)\n\n\n<!-- GETTING STARTED -->\n## Getting Started\n\n### Prerequisites\n\n`Poetry` is used for managing project dependencies, you can install it by: \n```\npip install poetry\n```\n\n### Installation\n* Clone the repo\n```\ngit clone https://gitlab.com/mwozniak11121/zlodziej-crawler-public.git\n```\n* Spawn poetry shell\n```sh\npoetry shell\n```\n* Install dependencies and package\n```sh\npoetry install\n```\n&nbsp;  \n\nOr if you want to install package through `pip`\n```sh\npip install zlodziej-crawler\n```\n\n<!-- USAGE EXAMPLES -->\n## Usage\n\nThe only script made available is `steal`, which prompts for `url` with offer's category, e.g.\n`olx.pl/nieruchomosci/mieszkania/wynajem/wroclaw/`  \nand then scraps, processes and saves found offers.\n(Results are saved in dir: `cwd / results`)\n\nExample output for `RentOffer` looks like this:\n![](docs/rent_offer.png)\n\n## Extending Project\nProject is meant to be easily extendable by adding new Pydantic models to `zlodziej_crawler/models.py`.  \n`BaseOffer` serves purpose as a generic offer for all types of offers that are not specificly processed.  \n`RentOffer` and its parent class `BaseOffer` look like this:\n\n```\nclass BaseOffer(BaseModel):\n    url: HttpUrl\n    offer_name: str\n    description: str\n    id: PositiveInt\n    time_offer_added: datetime\n    views: PositiveInt\n    location: str\n    price: Union[PositiveInt, str]\n    website: Optional[Website] = None\n    unused_data: Optional[Dict] = None\n\n\nclass RentOffer(BaseOffer):\n    rent: PositiveInt\n    area: float\n\n    number_of_rooms: Optional[str] = None\n    offer_type: Optional[OfferType] = OfferType.UNKNOWN\n    floor: Optional[str] = None\n    building_type: Optional[BuildingType] = BuildingType.UNKNOWN\n    furnished: Optional[bool] = None\n\n    total_price: Optional[int] = None\n    price_per_m: Optional[PositiveFloat] = None\n    total_price_per_m: Optional[PositiveFloat] = None\n\n```\n\nProject can be simply extended by adding matching classes based on other categories at [olx.pl](http://olx.pl).  \nAdding new OfferType needs:\n   * Parsing functions in `zlodziej_crawler/olx/offers_extraction/NEW_OFFER.py`\n   * Factory function in `OLXParserFactory` (`zlodziej_crawler/olx/parser_factory.py`)\n   * Matching offer category url in `OLXParserFactory.get_parser` (`zlodziej_crawler/olx/parser_factory.py`)\n\nCurrently any information found by scraper in `titlebox-details` section and not yet processed is saved as `unused_data`.\n![](docs/unused_data.png)",
    'author': 'Mateusz Woźniak',
    'author_email': 'mwozniak11121@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/mwozniak11121/zlodziej-crawler-public',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
