import requests

from zlodziej_crawler import paths


def cache_get(url: str) -> bytes:
    source_dir = paths.CWD_PATH / "sources"
    source_dir.mkdir(exist_ok=True)

    file_name = url.split("/")[-1]
    file_path = source_dir / file_name

    if file_path.is_file():
        return file_path.read_bytes()
    else:
        response = requests.get(url)
        file_path.write_bytes(response.content)
        return response.content
