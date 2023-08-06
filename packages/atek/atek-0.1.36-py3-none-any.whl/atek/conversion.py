# %%
from typing import *
from toolz.curried import pipe, take, map, merge, curry
import itertools as it
from functools import singledispatch
import pandas as pd
import re

__all__ = "to_table transpose to_date to_num to_camel decamel add_under".split()

# %%
@singledispatch
def to_table(data: Iterable[Dict[str, Any]]) -> Iterator[Dict[str, Any]]:
    """Conversion function that takes either a
        pandas DataFrame,
        Iterable of Dicts,
        dict,
        or string
    and converts it into an iterator (generator) of records where each record
    is a dict with keys of type str and values of type Any.

    >>> data = [
    ...     {"fname": "Axl", "lname": "Rose", "Band": "Guns 'n' Roses"},
    ...     {"fname": "Angus", "lname": "Young", "Band": "AC/DC"},
    ...     {"fname": "Steven", "lname": "Tyler", "Band": "Aerosmith"},
    ... ]
    # Returns an iterator (generator)
    >>> to_table(data)
    <generator object to_table at 0x10c101eb0>
    # Use list to visualize the data
    >>> list(to_table(data))
    [
        {'fname': 'Axl', 'lname': 'Rose', 'Band': "Guns 'n' Roses"},
        {'fname': 'Angus', 'lname': 'Young', 'Band': 'AC/DC'},
        {'fname': 'Steven', 'lname': 'Tyler', 'Band': 'Aerosmith'}
    ]
    >>> list(to_table(data[0]))
    [
        {'column': 'fname', 'value': 'Axl'},
        {'column': 'lname', 'value': 'Rose'},
        {'column': 'Band', 'value': "Guns 'n' Roses"}
    ]
    >>> list(to_table("Axl Rose"))
    [{'value': 'Axl Rose'}]
    >>> df = pd.DataFrame.from_records(data)
    >>> df
        fname  lname            Band
    0     Axl   Rose  Guns 'n' Roses
    1   Angus  Young           AC/DC
    2  Steven  Tyler       Aerosmith
    >>> list(to_table(df))
    [
        {'fname': 'Axl', 'lname': 'Rose', 'Band': "Guns 'n' Roses"},
        {'fname': 'Angus', 'lname': 'Young', 'Band': 'AC/DC'},
        {'fname': 'Steven', 'lname': 'Tyler', 'Band': 'Aerosmith'}
    ]
    """
    for row in data:
        yield row


@to_table.register(dict)
def _(data: Dict[str, Any]) -> Iterator[Dict[str, Any]]:
    for k, v in data.items():
        yield {"column": k, "value": v}


@to_table.register(str)
def _(data: str) -> Iterator[Dict[str, Any]]:
    yield {"value": data}


@to_table.register(pd.DataFrame)
def _(data: pd.DataFrame) -> Iterator[Dict[str, Any]]:
    for row in data.to_dict("records"):
        yield row


# %%
@singledispatch
def transpose(data: Iterable[Dict[str, Any]], limit: int=3
    ) -> Iterable[Dict[str,Any]]:
    """Transposes a table (list of dicts) such that columns are
    rows and rows are columns.

    from atek.conversion import *
    >>> import pandas as pd
    >>> data = [
    ...     {"fname": "Axl", "lname": "Rose", "Band": "Guns 'n' Roses"},
    ...     {"fname": "Angus", "lname": "Young", "Band": "AC/DC"},
    ...     {"fname": "Steven", "lname": "Tyler", "Band": "Aerosmith"},
    ... ]
    >>> list(transpose(data))
    [
        {'column': 'fname', 'row 1': 'Axl', 'row 2': 'Angus', 'row 3': 'Steven'},
        {'column': 'lname', 'row 1': 'Rose', 'row 2': 'Young', 'row 3': 'Tyler'},
        {'column': 'Band', 'row 1': "Guns 'n' Roses", 'row 2': 'AC/DC', 'row 3': 'Aerosmith'}
    ]
    >>> list(transpose(data[0]))
    [
        {'column': 'fname', 'row 1': 'Axl'},
        {'column': 'lname', 'row 1': 'Rose'},
        {'column': 'Band', 'row 1': "Guns 'n' Roses"}
    ]
    >>> list(transpose("Axl Rose"))
    [{'column': "'Axl Rose'", 'row 1': 'Axl Rose'}]
    >>> pd.DataFrame.from_records(data)
        fname  lname            Band
    0     Axl   Rose  Guns 'n' Roses
    1   Angus  Young           AC/DC
    2  Steven  Tyler       Aerosmith
    >>> df = pd.DataFrame.from_records(data)
    >>> df
        fname  lname            Band
    0     Axl   Rose  Guns 'n' Roses
    1   Angus  Young           AC/DC
    2  Steven  Tyler       Aerosmith
    >>> transpose(df)
    column           row 0  row 1      row 2
    0  fname             Axl  Angus     Steven
    1  lname            Rose  Young      Tyler
    2   Band  Guns 'n' Roses  AC/DC  Aerosmith
    """

    # Add a row number to each row of the data
    count = it.count(1)
    row_num = lambda: next(count)

    # Put the keys into a list
    header = lambda d: list(d.keys())

    # Put the list of values from 1 row into a list of many rows where each
    # value is a single row
    values = lambda d: list(zip(*d.values()))

    # Add the header value to each set of rows
    combine = lambda d: [dict(zip(header(d), row)) for row in values(d)]

    # Return the Table as a list of dict records
    return pipe(
        data
        ,take(limit)
        ,map(lambda row: list(zip(*row.items())))
        ,map(lambda row: dict(zip(["column", f"row {row_num()}"], row)))

        # Merge each record into 1 dict where the keys are the column
        # and row numbers
        ,merge
        ,combine
    )


@transpose.register(pd.DataFrame)
def _(data: pd.DataFrame, limit: int=3) -> pd.DataFrame:
    return pipe(
        data
        .head(limit)

        # Switch columns to rows and rows to columns
        .transpose()

        # Reset the index so that the column containing for column names
        # is named 'index'
        .reset_index()

        # Rename columns using index number as the 'row {col}' part
        ,lambda df: df.rename(columns={
            col: ("column" if col == "index" else f"row {int(col)+1}")
            for col in df.columns
        })
    )


@transpose.register(dict)
def _(data: Dict[str, Any]) -> Iterator[Dict[str, Any]]:
    for k, v in data.items():
        yield {"column": k, "row 1": v}


@transpose.register(str)
def _(data: str) -> Iterator[Dict[str, Any]]:
    yield {"value": data, "row 1": str(data)}

# %%
@curry
def to_date(pat: str, df: pd.DataFrame) -> pd.DataFrame:
    """Converts a 1 or more series in a DataFrame to a datetime64
    by applying pandas.to_datetime(errors_"coerce").

    pat arg will match column names. 'date' will convert any column in the
    dataframe with the word 'date' to a datetime64 column.
    """
    return df.assign(**{
        col: pd.to_datetime(df[col], errors="coerce")
        for col in df.columns
        if re.search(pat, col)
    })

# %%
@curry
def to_num(pat: str, df: pd.DataFrame) -> pd.DataFrame:
    """Converts a 1 or more series in a DataFrame to a float64
    by applying pandas.to_numeric(errors_"coerce").

    pat arg will match column names. '*fee*' will convert any column in the
    dataframe with the word 'fee' to a float64 column.
    """
    return df.assign(**{
        col: pd.to_numeric(df[col], errors="coerce")
        for col in df.columns
        if re.search(pat, col)
    })


# %%
@curry
def to_camel(df: pd.DataFrame) -> pd.DataFrame:
    """Converts columns in a dataframe to camel case.

    If df has columns OrderDate, LoanNumber, TrackingNumber
    >>>list(df.columns)
    ["OrderDate", "LoanNumber", "TrackingNumber"]
    >>>to_camel(df)
    ["order_date", "loan_number", "tracking_number"]
    """
    return df.rename(columns={
        col: re.sub(
            "(?P<lower>[a-z])(?P<upper>[A-Z])",
            "\g<lower>_\g<upper>",
            col
            ).lower()
        for col in df.columns
    })


# %%
@curry
def decamel(pats: Optional[Union[List[str],str]], df: pd.DataFrame) -> pd.DataFrame:
    """Takes columns in camel case and converts them to capitlized versions with
    the underscore replaced with a space and 'pct' replaced with '%' and
    pats replaced with upper case versions.

    >>>list(df.columns)
    ["order_date", "tracking_id", "pct_orders"]
    >>>list(decamel(["id"], df).columns)
    ["Order Date", "Tracking ID", "% Orders"]
    """
    pats = (
        [pats] if isinstance(pats, str) else
        [] if pats is None else
        pats
    )
    return df.rename(columns={
        col: " ".join([
            (part.upper() if part in pats else part.capitalize())
            .replace("Pct", "%")
            for part in col.split("_")
        ])
        for col in df.columns
    })


# %%
@curry
def add_under(pat: str, df: pd.DataFrame) -> pd.DataFrame:
    """Addes an underscore character before 'pat' if 'pat' is found at the end
    of the column name.

    >>>list(df.columns)
    ["trackingid", "loan_number", "idtracking"]
    >>>list(dunder(df).columns)
    ["tracking_id", "loan_number", "idtracking"]
    """
    return df.rename(columns={
        col: re.sub(
            f"(?P<lower>[a-z])(?P<pat>{pat})$",
            "\g<lower>_\g<pat>",
            col
        ).lower()
        for col in df.columns
    })

