import datetime
import json
import warnings
from typing import List

from zlodziej_crawler import paths
from zlodziej_crawler.models import BaseOffer


def export_offers(offers: List[BaseOffer], category_url: str):
    if not offers:
        warnings.warn("Extracted list of offers is empty!")

    category_path = paths.get_category_path(category_url)

    urls = list(set([str(offer.url) + "\n" for offer in offers]))
    global_file_urls = paths.get_urls_path()
    with open(global_file_urls, mode="a") as file:
        file.writelines(urls)

    ids = list(set([str(offer.id) + "\n" for offer in offers]))
    global_file_ids = paths.get_ids_path()
    with open(global_file_ids, mode="a") as file:
        file.writelines(ids)

    all_offers_path = category_path / "all_offers.json"
    current_offers = (
        json.loads(all_offers_path.read_text()) if all_offers_path.is_file() else []
    )
    all_offers = [offer.json(indent=4) for offer in offers] + [
        json.dumps(offer, indent=4) for offer in current_offers
    ]
    with open(all_offers_path, mode="w") as file:
        file.write("[")
        file.write(",\n".join(all_offers))
        file.write("]")

    session_name = _generate_dir_name()
    session_dir = category_path / session_name
    session_dir.mkdir(exist_ok=True)
    for offer in offers:
        file_name = str(offer.id) + ".json"
        file_path = session_dir / file_name
        with open(file_path, "w") as file:
            file.write(offer.json(indent=4))


def _generate_dir_name() -> str:
    return datetime.datetime.now().strftime("%m-%d-%Y___%H-%M-%S")
