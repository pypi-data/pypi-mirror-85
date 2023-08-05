from functools import wraps
from pathlib import Path
from typing import Callable

CWD_PATH = Path.cwd()
RESULTS_PATH = CWD_PATH / "results"


def make_sure_dir_exists(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        path: Path = func(*args, **kwargs)
        path.mkdir(exist_ok=True, parents=True)
        return path

    return wrapper


def make_sure_file_exists(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        path: Path = func(*args, **kwargs)
        path.parent.mkdir(exist_ok=True, parents=True)
        path.touch(exist_ok=True)
        return path

    return wrapper


@make_sure_dir_exists
def get_category_path(category_url: str) -> Path:
    dirs = category_url.split("/")
    return RESULTS_PATH.joinpath(*dirs)


@make_sure_file_exists
def get_ids_path() -> Path:
    return RESULTS_PATH / "ids_parsed.txt"


@make_sure_file_exists
def get_urls_path() -> Path:
    return RESULTS_PATH / "urls_parsed.txt"
