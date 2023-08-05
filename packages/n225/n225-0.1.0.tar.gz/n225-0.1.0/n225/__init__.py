"""n225 - Get compositions and josuu."""

__version__ = "0.1.0"
__author__ = "fx-kirin <fx.kirin@gmail.com>"
__all__ = ["get_compositions"]

import csv
import datetime
import functools
import os
from pathlib import Path

import diskcache
import ring

DISKCACHE_DIRECTORY = Path("~/.diskcache").expanduser()
if not DISKCACHE_DIRECTORY.exists():
    DISKCACHE_DIRECTORY.mkdir()

storage = diskcache.Cache(DISKCACHE_DIRECTORY)


def get_compositions(date):
    return _get_compositions(date.year, date.month, date.day)


@functools.lru_cache(maxsize=None)
@ring.disk(storage)
def _get_compositions(year, month, day):
    csv_path = Path(__file__).parents[1] / "data/n225.csv"
    with csv_path.open() as f:
        csv_obj = csv.reader(f)
        date = datetime.date(year, month, day)
