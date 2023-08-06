#  Copyright 2019 Michael Kemna.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
import os
from contextlib import contextmanager
from typing import List

from sqlalchemy import create_engine, MetaData, Table, Column
from sqlalchemy.engine import Engine, Connection, ResultProxy

from powderbooking.models import model_resort, model_weather, model_forecast, model_forecast_week
from powderbooking.query import Query
from powderbooking.utils import get_env_or_raise


class DatabaseHandler:
    """
    Database handler to manage all powderbooking interactions in one place.

    inspired by: https://github.com/rshk/flask-sqlalchemy-core/
    """
    engine: Engine
    metadata: MetaData

    def __init__(self, engine: Engine, metadata: MetaData):
        self.engine, self.metadata = engine, metadata

    @contextmanager
    def connect(self) -> Connection:
        """
        Connect to the powderbooking, ensures that the connection is closed once all transactions have occurred.
        """
        with self.engine.connect() as conn:
            yield conn
            conn.close()

    def execute(self, *args, **kwargs) -> ResultProxy:
        """
        Execute the inserted args and kwargs onto the powderbooking and return the ResultProxy.
        """
        with self.connect() as conn:
            return conn.execute(*args, **kwargs)

    def execute_query(self, query: Query, *args, **kwargs) -> ResultProxy:
        """
        Execute the pre-specified query.

        :param query: the Query that should be executed.
        :param args: any other positional arguments.
        :param kwargs: any other keyword arguments.
        :return: the ResultProxy.
        """
        return self.execute(query.value, *args, **kwargs)

    def get_table(self, table_name: str) -> Table:
        """
        Get the table from the metadata.

        :param table_name: the name of the table that should be retrieved
        :return: the Table object.
        """
        if table_name not in self.metadata.tables.keys():
            raise ValueError(f'{table_name} not in the tables of powderbooking')
        return self.metadata.tables[table_name]

    def get_table_column(self, table_name: str, column_name: str) -> Column:
        """
        Get the column of the particular table from the metadata.

        :param table_name: the name of the table that
        :param column_name: the name of the column that should be retrieved
        :return: the Column object.
        """
        table = self.get_table(table_name=table_name)
        if column_name not in table.columns:
            raise ValueError(f'{column_name} not in the columns of the table {table_name} of powderbooking')
        return table.columns[column_name]

    def insert(self, table_name: str, values: List[dict]) -> ResultProxy:
        """
        Insert the inserted list of values into the table that is given.
        Will raise a ValueError if the table is not inside the powderbooking.

        :param table_name: the name of the table that should be inserted into.
        :param values: a list of new rows that should be inserted.
        :return: the ResultProxy.
        """
        return self.execute(self.get_table(table_name).insert(), values)


def build_database_url() -> str:
    """
    Build the database url. Credentials are built from environmental variables.
    If any of the environmental variables aren't available, it will throw an EnvironmentError.

    :return: the database url
    """
    project = get_env_or_raise('PROJECT_NAME')
    username = get_env_or_raise('POSTGRESQL_USER')
    password = get_env_or_raise('POSTGRESQL_PASSWORD')
    host = get_env_or_raise(f'{project}_POSTGRESQL_SERVICE_HOST'.upper())
    port = get_env_or_raise(f'{project}_POSTGRESQL_SERVICE_PORT'.upper())
    database = get_env_or_raise('POSTGRESQL_DATABASE')
    return f'postgresql://{username}:{password}@{host}:{port}/{database}'


def build_database_handler(database_url: str) -> DatabaseHandler:
    """
    Build a DatabaseHandler from the given database url.
    This will create an SqlAlchemy engine and add the models.

    :param database_url: the url to the postgres database that should be handled.
    :return: a DatabaseHandler connected to the postgres database.
    """
    return DatabaseHandler(*create_model_database(database_url))


def create_model_database(database_url: str) -> (Engine, MetaData):
    return model_database(create_engine(database_url))


def model_database(engine: Engine, metadata: MetaData = MetaData()) -> (Engine, MetaData):
    """
    Enhance the metadata with the models that are relevant to Powderbooking, and create them on the engine.

    :param engine: the SqlAlchemy Engine that should be modeled
    :param metadata: the SqlAlchemy MetaData that should be modeled
    :return: the given Engine, and MetaData that have been applied to it.
    """
    model_resort(metadata)
    model_weather(metadata)
    model_forecast(metadata)
    model_forecast_week(metadata)

    metadata.create_all(engine)

    return engine, metadata
