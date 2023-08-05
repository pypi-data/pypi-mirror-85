import datetime
from pprint import pformat
from typing import List

import click
from pygments import highlight
from pygments.formatters import get_formatter_by_name
from pygments.lexers import get_lexer_by_name
from tqdm import tqdm

from zlodziej_crawler.models import Website, BaseOffer
from zlodziej_crawler.olx.crawler import OLXCrawler
from zlodziej_crawler.olx.parser_factory import OLXParsersFactory
from zlodziej_crawler.tools.export import export_offers
from zlodziej_crawler.tools.utilities import (
    filter_out_urls,
    filter_out_seen_urls,
)
from zlodziej_crawler.utilities import extract_category_url

WEBSITE = Website.OLX


def process_offers(category_url: str) -> List[BaseOffer]:
    crawler = OLXCrawler()
    parser = OLXParsersFactory.get_parser(category_url)
    page_url = WEBSITE.value

    valid_offers, invalid_offers = filter_out_urls(
        crawler.get_offers(category_url), page_url
    )
    if not valid_offers:
        raise ValueError("Extracted list of urls is empty!")

    new_urls = filter_out_seen_urls(valid_offers)
    additional_data = {"strona": page_url}

    offers: List[BaseOffer] = []
    processed_ids: List[int] = []
    progress_bar = tqdm(new_urls)
    for url in progress_bar:
        progress_bar.set_description(
            f"Currently scraping {page_url}/{category_url}", refresh=True
        )
        offer = parser.process_url(url, additional_data)
        if offer.id not in processed_ids:
            offers.append(offer)
            processed_ids.append(offer.id)

    return offers


@click.command()
@click.option(
    "--url",
    default="olx.pl/nieruchomosci/mieszkania/wynajem/wroclaw/",
    help="Enter category url to scrap",
    prompt=True,
)
def main(url: str):
    start = datetime.datetime.now()

    category_url = extract_category_url(url)
    offers = process_offers(category_url)
    export_offers(offers, category_url)

    json_output = [offer.dict() for offer in offers[-10:]]
    print(
        highlight(
            pformat(json_output),
            get_lexer_by_name("python"),
            get_formatter_by_name("terminal"),
        )
    )

    end = datetime.datetime.now()
    print(
        f"Scraped {len(offers)} new offers for {url} in {(end - start).total_seconds()} seconds"
    )


if __name__ == "__main__":
    main()
