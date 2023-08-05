from typing import List, Tuple

from zlodziej_crawler.paths import get_urls_path


def filter_out_urls(urls: List[str], page_url: str) -> Tuple[List[str], List[str]]:
    valid = [url for url in urls if page_url in url]
    invalid = [url for url in urls if page_url not in url]
    return valid, invalid


def filter_out_seen_urls(urls: List[str]) -> List[str]:
    urls_path = get_urls_path()
    processed_urls = set(urls_path.read_text().split("\n"))
    return [url for url in urls if url not in processed_urls]
