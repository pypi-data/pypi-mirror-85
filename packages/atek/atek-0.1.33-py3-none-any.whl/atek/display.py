from tabulate import tabulate
from atek.conversion import *
from typing import *
from textwrap import fill
from functools import singledispatch
import toolz.curried as tz
import pandas as pd

__all__ = ["show"]


def wrap(value: Any, width: int) -> str:
    return fill(str(value), width=width)


def wrapped(d: Dict[str, Any], width: int) -> Dict[str,str]:
    assert isinstance(d, dict), f"param 'd' must be a dict, provided {d}"
    return {
        wrap(k, width): wrap(v, width)
        for k, v in d.items()
    }


@singledispatch
def show(data: Iterable[Dict[str,Any]], *, caption: str="", limit: int=20,
    column_width: int=20, print_: bool=True, **tabulate_args
    ) -> str:

    # Default args for tabulate function
    default_args = {
        "tablefmt": "fancy_grid",
        "headers": "keys"
    }

    # Combine any passed args to default args for tabulate
    args = (
        tz.merge(default_args, tabulate_args) if tabulate_args else
        default_args
    )

    # Add caption if there is one
    table = f"\n{caption}\n" if caption else "\n"
    # Limit, wrap, and get results of tabulate
    table += tz.pipe(
        data
        ,tz.take(limit)
        ,tz.map(tz.partial(wrapped, width=column_width))
        ,list
        ,tz.partial(tabulate, **args)
    )

    # Returns the str result of tabulate if print_ set
    # Used for debugging and testing purposes
    if print_:
        print(table)
        return None
    return table


@show.register(dict)
@show.register(str)
@show.register(pd.DataFrame)
def _(data, **kwargs):
    return show(to_table(data), **kwargs)