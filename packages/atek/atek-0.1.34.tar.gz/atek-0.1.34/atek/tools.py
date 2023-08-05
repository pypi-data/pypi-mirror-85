#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
from fnmatch import fnmatch
from tabulate import tabulate
from textwrap import fill
from typing import *
import atek
from pathlib import Path
from dateutil.relativedelta import relativedelta as delta
from datetime import date, datetime
import pandas as pd
import re
import toolz.curried as tz
#  import atek
import censusdata
import us


__all__ = (
    "valid_path delta ymd bom eom notebook_setup states counties "
    "state_county"
).split()


def valid_path(path: Union[str, Path]) -> Path:
    """Returns a valid pathlib.Path object or provides smart error message
    indicating which parts are valid (exist) and which parts do not exist."""
    _path = Path(path).expanduser()
    # If expanded path or directory exists then return the expanded path
    if _path.exists():
        return _path

    # If expanded path doesn't exist, return a helpful error message by
    # calculating the good part (exists) of the path and the bad part of
    # path
    temp = _path.parent
    while True:
        if temp.exists():
            bad_part = _path.relative_to(temp)
            raise ValueError(
                f"{_path} does not exist.\n"
                f"Good part = {temp}, \n"
                f"Bad part = {bad_part}"
            )
        temp = temp.parent


def notebook_setup():
    pd.set_option("display.max_columns", 300)
    pd.set_option("display.max_colwidth", 0)
    pd.set_option("display.max_rows", 1_000)
    pd.set_option("display.min_rows", 300)
    pd.set_option("display.date_yearfirst", True)
    pd.set_option("display.float_format", lambda value: f"{value:,.2f}")
    pd.set_option("display.precision", 2)


def ymd(dt: Optional[date]=None) -> str:
    """Formats a date as yyyy-mm-dd."""
    dt = dt or date.today()
    return dt.strftime("%Y-%m-%d")


def bom(dt: Optional[date]=None, months: int=0) -> date:
    """Returns the first day of the month.
    dt -> change day to 1 -> add months."""
    dt = dt or date.today()
    return dt + delta(day=1, months=months)


def eom(dt: Optional[date]=None, months: int=0) -> date:
    """Returns the last day of the month.
    dt -> change day to 1 -> add months + 1 -> subtract a day."""
    dt = dt or date.today()
    return dt + delta(day=1, months=months+1, days=-1)


def states() -> pd.DataFrame:
    """Returns a pandas dataframe of State FIPS codes, abbreviations, and
    state names.

    Data comes from the acs5 2015 census data.
    """
    return tz.pipe(
        censusdata.geographies(
            censusdata.censusgeo([("state", "*")]),
            "acs5",
            2015
        )
        ,lambda d: [
            {
                "State": k,
                "State_FIPS": v.params()[0][1],
                "State_ID": int(v.params()[0][1]),
            }
            for k, v in d.items()
        ]
        ,tz.map(lambda d: tz.assoc(d, "State2", us.states.lookup(d["State"]).abbr))
        ,pd.DataFrame.from_records
    )


def counties() -> pd.DataFrame:
    """Returns a pandas dataframe of County Names, Cleaned County names.

    Cleaned County Names = Words Borough, Parish, City, County, Census Area,
        Municipality, and Municipio (PR) have been removed.

    Data comes from the acs5 2015 census data.
    """
    return tz.pipe(
        censusdata.geographies(
            censusdata.censusgeo([("state", "*"), ("county", "*")]),
            "acs5",
            2015
        )
        ,lambda d: [
            {
                "County_State": k,
                "State_FIPS": v.params()[0][1],
                "County_FIPS": v.params()[1][1],
                "County_ID": int(v.params()[1][1]),
            }
            for k, v in d.items()
        ]
        ,pd.DataFrame.from_records
        ,lambda df: df
        .assign(**{
            "County_Full": lambda df: df.County_State.str.extract("(^.*)(?=,.)"),
        })
        .assign(**{
            "County": lambda df: df.County_Full.str
                .replace(" County", "")
                .replace(" and Borough", "")
                .replace(" Census Area", "")
                .replace(" Municipality", "")
                .replace(" Borough", "")
                .replace(" Parish", "")
                .replace(" City", "")
                .replace(" Municipio", ""),
            "State_County_FIPS": lambda df: df.apply(lambda row:
                row["State_FIPS"] + row["County_FIPS"],
                axis=1
            ),
            "State_County_ID": lambda df: df.State_County_FIPS.astype("int"),
        })
        .drop(columns=["County_State"])
    )


def state_county() -> pd.DataFrame:
    """Combines results of states() and counties() into 1 pandas dataframe.
    Data comes from the acs5 2015 census data.
    """
    return tz.pipe(
        states()
        .merge(counties(), on="State_FIPS", how="left")
        .assign(**{
            "State_County": lambda df: df.apply(lambda row:
                row["State2"] + "|" + row["County"],
                axis = 1,
            ),
        })
    )