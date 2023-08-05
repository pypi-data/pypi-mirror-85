# %%
from pydantic.types import DirectoryPath
from sshtunnel import open_tunnel, SSHTunnelForwarder
from operator import methodcaller
import pymysql
import pandas as pd
import requests
import toolz.curried as tz
from pathlib import Path
from typing import Dict, Any, Iterable, List, Callable, Type, Union
import sqlite3
from sqlite3 import Connection as SQLite
from pydantic import (
    BaseSettings,
    SecretStr,
    PositiveInt,
    FilePath,
    Field,
    DirectoryPath,
)
import logging

__all__ = ["Cache", "Domo", "MySQL", "SQLite", "query"]

# %%
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s %(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S",
# )


# %%
class Cache(BaseSettings):
    """Returns the paths  using the ATEK_CACHE environment variable for the module."""
    cache: DirectoryPath

    @property
    def query(self) -> Path:
        return self.cache / "query"

    @property
    def secrets(self) -> Path:
        return self.cache / "secrets"

    class Config:
        env_prefix = "ATEK_"

    def __truediv__(self, other: Union[Path,str]):
        return Path(self.cache) / other

# Cache()
# Cache() / "secrets"

# %%
class Domo(BaseSettings):
    client_id: str
    secret: SecretStr
    dataset_id: str
    _header: Dict
    _url: str

    class Config:
        underscore_attrs_are_private = True
        env_prefix = "domo_"
        env_file = Cache().query
        secrets_dir = Cache().secrets

    def __init__(self, **data) -> None:
        super().__init__(**data)
        # Authenticate
        auth_url = (
            "https://api.domo.com/oauth/token?"
            "grant_type=client_credentials&scope=data"
        )
        auth = requests.auth.HTTPBasicAuth(
            self.client_id,
            self.secret.get_secret_value()
        )
        auth_response = requests.get(auth_url, auth=auth)
        token = auth_response.json()["access_token"]
        logging.info(f"AUTHENTICATED: Domo")
        logging.debug(self)

        # Assemble post url
        self._header = {"Authorization": f"bearer {token}"}
        base_url = "https://api.domo.com/v1/datasets"
        self._url = (
            f"{base_url}/query/execute/{self.dataset_id}"
            "?includeHeaders=true"
        )

    def query(self, sql: str, *args, **kwargs) -> pd.DataFrame:
        logging.info(f"EXECUTING: Domo Query\n{sql}")
        results = requests.post(
            self._url,
            headers=self._header,
            json={"sql": sql}
            ).json()
        columns = results["columns"]
        rows = results["rows"]
        data = [
            dict(zip(columns, row))
            for row in rows
        ]
        logging.info(f"RETURNED: Domo Query")
        return pd.DataFrame.from_records(data)

# TODO: Add tables method
# TODO: Add col_info method
# TODO: Add DB API methods so that can be used with pandas.read_sql
# TODO: Add to_date, to_num methods to query

# sql = "select TrackingNumber, OrderDate from table limit 1"
# print(Domo().query(sql))


# %%
class MySQL(BaseSettings):
    remote_host: str="localhost"
    remote_port: PositiveInt=3306

    jump_host: str
    jump_port: PositiveInt=22
    jump_username: str
    jump_pkey: FilePath
    jump_password: SecretStr

    server_host: str
    server_port: PositiveInt=22
    server_username: str
    server_pkey: str
    server_password: SecretStr

    db_host: str="localhost"
    db_name: str
    db_username: str
    db_password: SecretStr

    kwargs: Dict=Field(default_factory=dict)

    _jump: SSHTunnelForwarder=None
    _server: SSHTunnelForwarder=None
    _connection: pymysql.connections.Connection=None
    _with_context: bool = False

    class Config:
        underscore_attrs_are_private = True
        env_prefix = "mysql_"
        env_file = Cache().query
        secrets_dir = Cache().secrets

    def __init__(self, **data) -> None:
        super().__init__(**data)

        self._jump = open_tunnel(
            ssh_address_or_host=(self.jump_host, self.jump_port),
            remote_bind_address=(self.remote_host, self.remote_port),
            ssh_pkey=str(self.jump_pkey),
            ssh_username=self.jump_username,
            ssh_password=self.jump_password.get_secret_value(),
        )
        self._jump.start()
        logging.info(f"OPENED: {self.jump_host}:{self.jump_port}")

        self._server = open_tunnel(
            ssh_address_or_host=(self.server_host, self.server_port),
            remote_bind_address=(self.remote_host, self.remote_port),
            ssh_pkey=self.server_pkey,
            ssh_username=self.server_username,
            ssh_password=self.server_password.get_secret_value(),
        )
        self._server.start()
        logging.info(f"OPENED: {self.server_host}:{self.server_port}")

        self._connection = pymysql.connect(
            host=self.db_host,
            db=self.db_name,
            user=self.db_username,
            password=self.db_password.get_secret_value(),
            port=self._server.local_bind_port,
            **self.kwargs
        )
        logging.info(f"OPENED: {self.db_host}:{self.db_name}")

    def close(self, *args, **kwargs) -> None:
        self._connection.close(*args, **kwargs)
        self._connection = None
        logging.info(f"CLOSED: {self.db_host}:{self.db_name}")

        self._server.stop()
        self._server = None
        logging.info(
            f"CLOSED: {self.server_host}:{self.server_port}")

        self._jump.stop()
        self._jump = None
        logging.info(f"CLOSED: {self.jump_host}:{self.jump_port}")

    @property
    def connection(self) -> pymysql.connections.Connection:
        return self._connection

    @property
    def conn(self) -> pymysql.connections.Connection:
        return self.connection

    def __enter__(self):
        self._with_context = True
        return self

    def __exit__(self, *args):
        self.close()
        self._with_context = False

    def query(self, sql: str, *args, **kwargs) -> pd.DataFrame:
        logging.info(f"EXECUTING: {self.db_host}:{self.db_name} Query\n{sql}")
        df = pd.read_sql(sql, self.conn, *args, **kwargs)
        logging.info(f"RETURNED: {self.db_host}:{self.db_name} Query")
        if not self._with_context:
            self.close()
        return df

# sql = "select current_user, current_timestamp"
# MySQL().query(sql)

# with MySQL() as conn:
#     conn.query(sql)
#     conn.query(sql)

# pd.read_sql(sql, MySQL().conn)


# %%
class SQLite(BaseSettings):
    path: FilePath
    kwargs: Dict=Field(default_factory=dict)
    _connection: sqlite3.Connection=None
    _with_context: bool = False

    class Config:
        underscore_attrs_are_private = True
        env_prefix = "sqlite_"
        env_file = Cache().query
        secrets_dir = Cache().secrets

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._connection = sqlite3.connect(self.path, **self.kwargs)
        logging.info(f"OPENED: {self.path}")

    def close(self) -> None:
        self._connection.close()
        self._connection = None
        logging.info(f"CLOSED: {self.path}")

    @property
    def connection(self) -> pymysql.connections.Connection:
        return self._connection

    @property
    def conn(self) -> pymysql.connections.Connection:
        return self.connection

    def __enter__(self):
        self._with_context = True
        return self

    def __exit__(self, *args):
        self.close()
        self._with_context = False

    def query(self, sql: str, *args, **kwargs) -> pd.DataFrame:
        logging.info(f"EXECUTING: {self.path} Query\n{sql}")
        df = pd.read_sql(sql, self.conn)
        logging.info(f"RETURNED: {self.path} Query")
        if not self._with_context:
            self.close()
        return df

    def tables(self) -> List[str]:
        return self.query("""
            select name as table_name
            from sqlite_master
            where type = 'table'
            """).table_name.tolist()

    def col_info(self, table_name: str) -> pd.DataFrame:
        if table_name not in self.tables():
            raise ValueError(f"{table_name} does not exist in {self.path}")
        return tz.pipe(
            self.query(f"pragma table_info({table_name})")
            .assign(**{"table": table_name})
            .rename(columns={"name": "column"})
            .filter(["table", "cid", "column", "type", "notnull"])
        )

    def schema(self) -> pd.DataFrame:
        return pd.concat([
            self.col_info(table)
            for table in self.tables()
        ])

# sql = "select sqlite_version() as version, date('now') as today"
# print(SQLite().query(sql))

# with SQLite() as conn:
#     print(conn.query(sql))

# print(pd.read_sql(sql, SQLite().conn))
# print(SQLite().schema())


# %%
def query(connection: Union[MySQL,SQLite,Domo], sql: str, *args, **kwargs) -> List[Dict]:
    return connection.query(sql, *args, **kwargs)

# print(query(Domo(), "select TrackingNumber, OrderDate from table limit 1"))
# print(query(MySQL(), "select current_user, current_timestamp"))
# print(query(SQLite(), "select sqlite_version() as version, date('now') as today"))
# %%
