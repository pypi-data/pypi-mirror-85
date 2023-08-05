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

DISKCACHE_DIRECTORY = Path("~/.diskcache/n225").expanduser()
if not DISKCACHE_DIRECTORY.exists():
    DISKCACHE_DIRECTORY.mkdir()

storage = diskcache.Cache(DISKCACHE_DIRECTORY)


def get_compositions(date):
    return _get_compositions(date.year, date.month, date.day)


@functools.lru_cache(maxsize=None)
@ring.disk(storage)
def _get_compositions(year, month, day):
    date = datetime.date(year, month, day)
    n225_dict = {"stocks": {}}
    init_csv_path = Path(__file__).parents[1] / "data/initial_n225.csv"
    with init_csv_path.open() as f:
        csv_obj = csv.reader(f)
        from_date = next(csv_obj)[1].strip()
        from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d").date()
        if date < from_date:
            raise NotImplementedError(f"Not implemnted n225 list before {from_date}")
        n225_dict["josuu"] = float(next(csv_obj)[1].strip())
        next(csv_obj)
        for row in csv_obj:
            n225_dict["stocks"][row[0].strip()] = row[1].strip()

    csv_path = Path(__file__).parents[1] / "data/n225.csv"
    with csv_path.open() as f:
        csv_obj = csv.reader(f)
        next(csv_obj)
        for row in csv_obj:
            mod_date = datetime.datetime.strptime(row[0].strip(), "%Y-%m-%d").date()
            if mod_date > date:
                break
            remove_stock = row[1].strip()
            add_stock = row[2].strip()
            minashi = row[3].strip()
            josuu = row[4].strip()
            del n225_dict["stocks"][remove_stock]
            n225_dict["stocks"][add_stock] = minashi
            n225_dict["josuu"] = float(josuu)

    assert len(n225_dict["stocks"]) == 225
    return n225_dict
