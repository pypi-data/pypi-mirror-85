"""Provides basic utilities to query a mysql database over an ssh tunnel"""
from sshtunnel import SSHTunnelForwarder, open_tunnel
import pandas as pd
import pymysql
from pymysql.cursors import Cursor, SSDictCursor
from pymysql.connections import Connection
from pathlib import Path
from typing import *
from configparser import ConfigParser
from contextlib import contextmanager
import os
import requests
from cytoolz.curried import pipe, partial, curry, get_in, take, map, merge

__all__ = "config query_atek02_main query_acad_domo".split()

def parse_config(config_path: str):
    """Reads a config file using configparser.ConfigParser from the standard library
    and converts any values with address in the key name to a ip address and port
    combination."""
    config = ConfigParser()
    path = Path(config_path).expanduser()
    config.read(path)
    settings = {
        section: {
            key: (
                tuple([
                    value.split()[0],
                    int(value.split()[1])
                ]) if "address" in key else
                value
            )
            for key, value in config[section].items()
        }
        for section in config.sections()
    }
    return settings


def config(env_var: str, *keys: str):
    """Returns the values in a config file as a dict or nested dict using an
    environment value ('env_var') which refers to a path.
    # 'path/to/some/config/file'
    [section 1]
    param1 = value1
    param2 = value2

    [section 2]
    parama = valuea
    paramb = valueb

    SOME_VAR='path/to/some/config/file'
    >>> config("SOME_VAR")
    {"section 1": {"param1": "value1", "param2": "value2"},
    "section 2": {"parama": "valuea", "paramb": "valueb"}}

    >>> config("SOME_VAR", "section 1")
    {"param1": "value1", "param2": "value2"}

    >>> config("SOME_VAR", "section 1", "param2")
    "value2"

    """
    # Get the enironment variable with a default of '' if it doesn't exist
    env_value = os.getenv(env_var, "")
    assert env_value != "", "f{env_var=} doesn't exist or returned ''"

    # Return the dict or potentially nested dict from parse_config
    settings = parse_config(env_value)

    # Return the value using nested keys
    return get_in([*keys], settings)


@contextmanager
def connect_atek02_main() -> Connection:
    """Creates a ssh tunnel and returns a connection options to atek02_main."""

    # Establish the ssh tunnel
    with SSHTunnelForwarder(**config("ATEK02_MAIN", "public_html")) as tunnel:

        # Create a connection to the database and a lazy cursor
        conn = pymysql.connect(
            **config("ATEK02_MAIN", "atek02_main"),
            port=tunnel.local_bind_port,
            cursorclass=SSDictCursor
        )

        yield conn

        conn.close()


Record = Dict[str,Any]
Table = Iterable[Record]

def query_atek02_main(sql: str) -> Table:
    """Returns a generator of dict objects as records."""

    with connect_atek02_main() as conn:
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall_unbuffered()
        for row in rows:
            yield row


def connect_acad_domo():
    """Returns an authorization header used in working with a domo
    instance api."""

    # Get client_id and token from config file and obtain an auth token
    domo = config("ACADEMY_DOMO", "acad_domo")
    auth = requests.auth.HTTPBasicAuth(domo["client_id"], domo["secret"])
    response = requests.get(domo["auth_url"], auth=auth)
    token = response.json()["access_token"]

    # Create and return the authorization header
    header = {"Authorization": f"bearer {token}"}
    return header


def datasets_acad_domo(name_or_id: Optional[str]=None,
    env_var: str="ACADEMY_DOMO") -> Table:
    """Retrieves a list of datasets from the domo instance for which the
    token has access."""

    header = connect_acad_domo()
    limit = 50
    offset = 0
    base_url = config(env_var, "acad_domo", "base_url")

    # Cycle through the list in chunks of 'limit'
    while True:
        url = f"{base_url}?offset={offset}&limit={limit}"
        chunk = requests.get(url, headers=header).json()
        if not chunk: break
        for row in chunk:
            # If name or id provided then only yield a row if it matches
            name = row["name"]
            id = row["id"]

            if name_or_id:
                if name_or_id == name or name_or_id == id:
                    yield row
                else:
                    pass

            # If name and id are not provided yield all rows
            else:
                yield row
        offset += limit


@curry
def query_acad_domo( name_or_id: Optional[str]=None, sql: Optional[str]=None):
    # Create the header
    header = connect_acad_domo()
    header["Accept"] = "application/json"
    name_or_id = name_or_id or "Prod - Appraisal - Mercury Appraisal No PDP"
    sql = sql or "select * from table"
    query = {"sql": sql}
    base_url = config("ACADEMY_DOMO", "acad_domo", "base_url")

    # Get thet table id
    table = list(datasets_acad_domo(name_or_id))
    assert len(table) > 0, "Returned dataset is empty... check the provided " \
        "'name_or_id' parameter."

    id = table[0]["id"]
    url = f"{base_url}/query/execute/{id}?includeHeaders=true"

    # Get the table in json formaatt
    response = requests.post(url, headers=header, json=query).json()

    # Assembe the table as a list of dict objects
    columns = response["columns"]
    rows = response["rows"]
    data = [
        dict(zip(columns, row))
        for row in rows
    ]

    # lazily return the data
    for row in data:
        yield row