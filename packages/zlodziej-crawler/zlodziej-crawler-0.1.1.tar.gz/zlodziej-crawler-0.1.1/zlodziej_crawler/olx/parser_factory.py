from zlodziej_crawler.models import BaseOffer, RentOffer
from zlodziej_crawler.olx.base_parser import BaseParser
from zlodziej_crawler.olx.offers_parsing.base_offer import mapping as base_mapping
from zlodziej_crawler.olx.offers_parsing.rent_offer import mapping as rent_mapping
from zlodziej_crawler.olx.scrap_data import functions_to_execute as scrap_functions


class OLXParsersFactory:
    @staticmethod
    def _get_empty_parser() -> BaseParser:
        return BaseParser(
            offer_class=BaseOffer,
            scrap_functions=scrap_functions,
            parse_functions=None,
        )

    @staticmethod
    def _get_base_offer_parser() -> BaseParser:
        mapping = base_mapping

        return BaseParser(
            offer_class=BaseOffer,
            scrap_functions=scrap_functions,
            parse_functions=mapping,
        )

    @staticmethod
    def _get_rent_offer_parser() -> BaseParser:
        mapping = {**base_mapping, **rent_mapping}

        return BaseParser(
            offer_class=RentOffer,
            scrap_functions=scrap_functions,
            parse_functions=mapping,
        )

    @staticmethod
    def get_parser(category_url: str) -> BaseParser:
        MAPPING = {"mieszkania/wynajem": OLXParsersFactory._get_rent_offer_parser}

        factory_function = OLXParsersFactory._get_base_offer_parser
        for category in MAPPING.keys():
            if category in category_url:
                factory_function = MAPPING[category]
                break

        return factory_function()
