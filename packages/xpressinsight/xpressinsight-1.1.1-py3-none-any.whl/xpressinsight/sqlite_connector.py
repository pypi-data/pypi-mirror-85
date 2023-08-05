"""
    Xpress Insight Python package
    =============================

    This is an internal file of the 'xpressinsight' package. Do not import it directly.

    (c) 2020 Fair Isaac Corporation
"""

import os
from typing import Any, Dict, Optional, Union, Type, ValuesView

import numpy as np
import pandas as pd
import sqlite3 as sql
from contextlib import contextmanager
import datetime

import xpressinsight.types as xi_types
from xpressinsight.app_base import DataConnector
from xpressinsight.interface_rest import AppRestInterface

#
#
#
TABLE_PREFIX_ENTITY = "ENTITY_"

SQLITE_FILENAME = "sqlite_connector.sqlite"

SingleValueDict = Dict[Type[xi_types.BasicType], Dict[str, Any]]
SPType = Union[Type[xi_types.Scalar], Type[xi_types.Param]]

SQL_TYPE_MAP: Dict[Type[xi_types.BasicType], str] = {
    xi_types.boolean: 'BOOLEAN',
    xi_types.integer: 'INT',
    xi_types.string: 'TEXT',
    xi_types.real: 'FLOAT',
}


def decode_identifier(ident: str):
    (x, _, _) = ident.rpartition("_")
    return x


def encode_identifier(ident: str):
    """Encode a valid identifier so that it can be used in a case insensitive SQL database (table or column name)"""
    tail = (
        np.packbits([int(c.isupper()) for c in ident], bitorder="little")
        .tobytes()
        .hex()
    )
    return "{}_{}".format(ident, tail)


def e_table_name(name):
    return TABLE_PREFIX_ENTITY + encode_identifier(name)


def ec_table_name(name: str, column: str):
    """Encode the name of the table for a DataFrame"""

    return TABLE_PREFIX_ENTITY + encode_identifier(name + "_" + column)


def ec_column_name(name: str, column: str):
    """Encode the name of the column for a DataFrame"""

    return encode_identifier(name + "_" + column)


def sp_table_name(sp_type: SPType, dtype: Type[xi_types.BasicType]):
    """Returns the table name"""

    return sp_type.__name__.upper() + "_" + dtype.__name__


class Sqlite3Connector(DataConnector):
    def __init__(self, app, sqlite_file: str):
        super().__init__(app)
        self._app = app
        self._entities: ValuesView[xi_types.EntityBase] = type(app).app_cfg.entities
        self._sqlite_file: str = sqlite_file
        self._conn: Optional[sql.Connection] = None
        self._verbose: bool = False

    def _load_scalars(self, manage: Optional[xi_types.Manage] = None):
        scalars = self._load_single_values_db("SCALAR")
        self._set_single_values_app(xi_types.Scalar, scalars, manage)

    def _load_params(self, manage: Optional[xi_types.Manage] = None):
        params = self._load_single_values_db("PARAM")
        self._set_single_values_app(xi_types.Param, params, manage)

    def _load(self, manage: Optional[xi_types.Manage] = None):
        """
        Reads from database and initializes attributes of app
        if manage is None then all entities are loaded
        if sp_type is None then also save scalars and params, otherwise save only given sp_type
        """

        for entity in self._entities:
            if isinstance(entity, (xi_types.Param, xi_types.Scalar)):
                pass  #

            else:
                if isinstance(entity, xi_types.Index) and (manage is None or entity.is_managed(manage)):
                    table_name = e_table_name(entity.name)
                    df = self._import_table(table_name)
                    df.columns = [decode_identifier(c) for c in df.columns]

                    #
                    value = df.set_index(entity.name).index
                    xi_types.check_type(value, entity, entity.name, manage)
                    self._app.__dict__[entity.name] = value

                elif isinstance(entity, xi_types.Series) and (manage is None or entity.is_managed(manage)):
                    table_name = e_table_name(entity.name)
                    df = self._import_table(table_name)
                    df.columns = [decode_identifier(c) for c in df.columns]

                    #
                    #
                    index = [index.name for index in entity.index]
                    value = df.set_index(index)[entity.name]
                    xi_types.check_type(value, entity, entity.name, manage)
                    self._app.__dict__[entity.name] = value

                elif isinstance(entity, xi_types.DataFrame):
                    #
                    if manage is None:
                        columns = entity.columns
                    else:
                        columns = [c for c in entity.columns if c.is_managed(manage)]

                    if columns:
                        index = [index.name for index in entity.index]
                        df_full: pd.DataFrame = pd.DataFrame()

                        #
                        for c in columns:
                            table_name = ec_table_name(entity.name, c.name)
                            df = self._import_table(table_name)

                            #
                            rename_map = {encode_identifier(index.name): index.name for index in entity.index}
                            rename_map[ec_column_name(entity.name, c.name)] = c.name
                            df = df.rename(columns=rename_map)
                            sr = df.set_index(index)[c.name]

                            df_full[c.name] = sr

                        xi_types.check_type(df_full, entity, entity.name, manage)

                        #
                        #
                        if entity.name in self._app.__dict__:
                            df_org = self._app.__dict__[entity.name]

                            if isinstance(df_org, pd.DataFrame):
                                for col_label, col in df_org.iteritems():
                                    #
                                    if col_label not in df_full.columns:
                                        df_full[col_label] = col

                        #
                        self._app.__dict__[entity.name] = df_full

    def _save_encoded(
        self,
        entity: Union[xi_types.Index, xi_types.Series, xi_types.DataFrame],
        value: Union[pd.DataFrame, pd.Series, pd.Index],
        manage: Optional[xi_types.Manage] = None,
    ):
        entity_name = entity.name

        if isinstance(value, pd.Index):
            #
            ser = value.to_series()
            ser.name = encode_identifier(entity_name)
            dtype = {ser.name: SQL_TYPE_MAP[entity.dtype]}
            table_name = e_table_name(entity_name)

            self._export_table(ser, table_name, index=False, dtype=dtype)

        elif isinstance(value, pd.Series):
            #
            #
            norm_name = entity_name
            enc_col_name = encode_identifier(norm_name)
            value.name = enc_col_name
            dtype = {encode_identifier(ind.name): SQL_TYPE_MAP[ind.dtype] for ind in entity.index}
            value.index.names = list(dtype.keys())
            dtype[enc_col_name] = SQL_TYPE_MAP[entity.dtype]
            table_name = e_table_name(entity_name)

            try:
                self._export_table(value, table_name, dtype=dtype)
            finally:
                value.name = norm_name
                value.index.names = [ind.name for ind in entity.index]

        elif isinstance(value, pd.DataFrame):
            if manage is None:
                columns = entity.columns
            else:
                columns = [c for c in entity.columns if c.is_managed(manage)]

            for c in columns:
                #
                sr = value[c.name]

                #
                norm_name = c.name
                enc_col_name = ec_column_name(entity_name, norm_name)
                sr.name = enc_col_name
                dtype = {encode_identifier(ind.name): SQL_TYPE_MAP[ind.dtype] for ind in entity.index}
                sr.index.names = list(dtype.keys())
                dtype[enc_col_name] = SQL_TYPE_MAP[c.dtype]
                table_name = ec_table_name(entity_name, c.name)

                try:
                    self._export_table(sr, table_name, dtype=dtype)
                finally:
                    sr.name = norm_name
                    sr.index.names = [ind.name for ind in entity.index]

    def _save_scalars(self, manage: Optional[xi_types.Manage] = None):
        scalars = self._get_single_values_app(xi_types.Scalar, manage)

        #
        if manage == xi_types.Manage.RESULT:
            old_scalars = self._load_single_values_db("SCALAR")

            for entity in self._entities:
                if isinstance(entity, xi_types.Scalar) and\
                        entity.manage == xi_types.Manage.INPUT and not entity.update_after_execution:
                    #
                    old_value = old_scalars[entity.dtype].get(entity.name)

                    if old_value is not None:
                        scalars[entity.dtype][entity.name] = old_value

        self._save_single_values_db("SCALAR", scalars)

    def _save_params(self, manage: Optional[xi_types.Manage] = None):
        params = self._get_single_values_app(xi_types.Param, manage)
        self._save_single_values_db("PARAM", params)

    def _save(self, manage: Optional[xi_types.Manage] = None):
        """
        Writes managed attributes of app to database. Does not save scalars or params.
        @param manage: If manage is None then all entities are saved.
        """

        for entity in self._entities:
            if manage is None or entity.is_managed(manage):
                if entity.name not in self._app.__dict__:
                    raise KeyError("Entity {} declared but not initialized.".format(entity.name))

                entity_value = self._app.__dict__[entity.name]
                xi_types.check_type(entity_value, entity, entity.name, manage)

                if isinstance(entity, (xi_types.Index, xi_types.Series, xi_types.DataFrame)):
                    self._save_encoded(entity, entity_value, manage)
                elif isinstance(entity, (xi_types.Param, xi_types.Scalar)):
                    pass  #
                else:
                    raise RuntimeError("Unexpected entity type: {}".format(type(entity).__name__))

    def _clean_db(self):
        """Function which creates directory structure for the SQLite database
        (if it does not exist. If there is an existing database already present, it is deleted."""

        #
        os.makedirs(self._app.insight.work_dir, exist_ok=True)

        if os.path.isfile(self._sqlite_file):
            os.remove(self._sqlite_file)

    def _does_db_exist(self):
        """Returns True iff database file exists"""
        return os.path.isfile(self._sqlite_file)

    def _check_db_exists(self):
        """Checks if the SQLite database files exists, if it does not, raises and exception"""

        if not self._does_db_exist():
            raise FileNotFoundError("Cannot find database {}".format(self._sqlite_file))

    def _init_default_values(self, sp_type: SPType):
        """
        Set uninitialized scalars/parameters/meta data to default values.
        If sp_type == None then initialize both Scalar and Param, otherwise initialize only of given type.
        """

        for entity in self._entities:
            if isinstance(entity, sp_type):
                #
                if entity.manage == xi_types.Manage.RESULT or\
                        entity.name not in self._app.__dict__:
                    self._app.__dict__[entity.name] = entity.default

    def _get_single_values_app(
        self, sp_type: SPType, manage: Optional[xi_types.Manage] = None
    ) -> SingleValueDict:

        values = {t: {} for t in xi_types.ALL_BASIC_TYPE}

        for entity in self._entities:
            if isinstance(entity, sp_type) and (manage is None or entity.is_managed(manage)):
                if entity.name not in self._app.__dict__:
                    raise KeyError(
                        "Entity {} declared but not initialized.".format(entity.name)
                    )

                entity_value = self._app.__dict__[entity.name]
                xi_types.check_type(entity_value, entity, entity.name, manage)
                values[entity.dtype][entity.name] = entity_value

        return values

    def _set_single_values_app(
        self,
        sp_type: SPType,
        values: SingleValueDict,
        manage: Optional[xi_types.Manage] = None,
    ):

        for entity in self._entities:
            if isinstance(entity, sp_type) and (manage is None or entity.is_managed(manage)):
                if entity.name not in values[entity.dtype]:
                    msg = "{} {} (of type {}) does not exist in the database.".format(
                        "Parameter" if entity.dtype == xi_types.Param else "Scalar",
                        entity.name,
                        entity.dtype.__name__,
                    )
                    raise ValueError(msg)

                value = values[entity.dtype][entity.name]

                xi_types.check_type(value, entity, entity.name, manage)
                self._app.__dict__[entity.name] = value

    def _save_single_values_db(self, prefix: str, values: SingleValueDict):
        """Saves SingleValueDict to the database"""

        assert prefix in ("SCALAR", "PARAM", "META")

        for dtype in xi_types.ALL_BASIC_TYPE:
            #
            if dtype in values and values[dtype]:
                table_name = "{}_{}".format(prefix, dtype.__name__)

                df = pd.DataFrame(
                    values[dtype].items(), columns=["Name", "Value"]
                ).set_index("Name")
                dtype = {
                    "Name": SQL_TYPE_MAP[xi_types.string],
                    "Value": SQL_TYPE_MAP[dtype],
                }
                self._export_table(df, table_name, dtype=dtype)

    def _has_table(self, table_name: str):
        #
        cur = self._conn.execute('SELECT name FROM sqlite_master WHERE type="table" and name=?', [table_name])
        num_tables = len(cur.fetchall())
        cur.close()
        return num_tables > 0

    def _get_table_info(self, table_name: str) -> pd.DataFrame:
        return pd.read_sql_query(f'PRAGMA table_info("{xi_types.validate_raw_ident(table_name)}")', self._conn)

    def _import_table(self, table_name: str) -> pd.DataFrame:
        start_time = datetime.datetime.utcnow()

        #
        select_table = f'SELECT * FROM "{xi_types.validate_raw_ident(table_name)}"'
        table = pd.read_sql_query(select_table, self._conn)
        table_info = self._get_table_info(table_name)

        for _, row in table_info.iterrows():
            col_dtype = row['type'].upper()

            if col_dtype == SQL_TYPE_MAP[xi_types.boolean]:
                #
                col_name = row['name']
                table[col_name] = table[col_name].astype(np.bool, copy=False)
            if table.size == 0:
                #
                if col_dtype == SQL_TYPE_MAP[xi_types.integer]:
                    col_name = row['name']
                    table[col_name] = table[col_name].astype(np.int64, copy=False)
                elif col_dtype == SQL_TYPE_MAP[xi_types.real]:
                    col_name = row['name']
                    table[col_name] = table[col_name].astype(np.float64, copy=False)
                #
                #

        if self._verbose:
            end_time = datetime.datetime.utcnow()
            print('Imported {}: {}'.format(table_name, end_time - start_time))

        return table

    def _export_table(self, df: Union[pd.DataFrame, pd.Series], table_name: str, dtype: Dict[str, str],
                      index: bool = True):
        start_time = datetime.datetime.utcnow()

        self._conn.execute(f'DROP TABLE IF EXISTS "{xi_types.validate_raw_ident(table_name)}"')
        table_columns = ', '.join(
            (f'"{xi_types.validate_raw_ident(idx_name)}" {xi_types.validate_raw_ident(idx_dtype)}'
             for idx_name, idx_dtype in dtype.items()))
        self._conn.execute(f'CREATE TABLE "{table_name}" ({table_columns})')

        df.to_sql(table_name, self._conn, if_exists="append", dtype=dtype, index=index)

        if self._verbose:
            end_time = datetime.datetime.utcnow()
            print('Exported {}: {}'.format(table_name, end_time - start_time))

    def _load_single_values_db(self, prefix: str) -> SingleValueDict:
        """Loads from the database and returns SingleValueDict"""

        assert prefix in ("SCALAR", "PARAM", "META")

        values = {}

        for dtype in xi_types.ALL_BASIC_TYPE:
            table_name = "{}_{}".format(prefix, dtype.__name__)

            if self._has_table(table_name):
                df = self._import_table(table_name)

                if ("Name" not in df.columns) or ("Value" not in df.columns):
                    raise KeyError(
                        "Table {} must have 'Name' and 'Value' columns, it has {}.".format(
                            table_name, df.columns
                        )
                    )

                values[dtype] = {
                    name: value for (name, value) in zip(df["Name"], df["Value"])
                }
            else:
                values[dtype] = {}

        #
        values[xi_types.boolean] = {
            name: xi_types.python_int_to_bool(value)
            for name, value in values[xi_types.boolean].items()
        }

        return values

    def _load_meta(self):

        meta_values = self._load_single_values_db("META")

        if isinstance(self._app.insight, AppRestInterface):
            rest_port = meta_values[xi_types.integer]['http_port']
            rest_token = meta_values[xi_types.string]['http_token']
            #
            self._app.insight._init_rest(rest_port, rest_token)

        meta_values_str = meta_values[xi_types.string]

        #
        if 'app_id' in meta_values_str:
            self._app.insight._app_id = meta_values_str['app_id']

        if 'app_name' in meta_values_str:
            self._app.insight._app_name = meta_values_str['app_name']

        if 'scenario_id' in meta_values_str:
            self._app.insight._scenario_id = meta_values_str['scenario_id']

        if 'scenario_name' in meta_values_str:
            self._app.insight._scenario_name = meta_values_str['scenario_name']

        if 'scenario_path' in meta_values_str:
            self._app.insight._scenario_path = meta_values_str['scenario_path']

    def _load_params_and_meta(self):

        self._load_meta()
        self._load_params()

    def _warn_about_work_dir(self):
        if os.path.isdir(self._app.insight.work_dir):
            print("Test mode: Using existing Insight working directory.")

    @contextmanager
    def _connect(self):
        """ Connect to a DB and disconnect when finished. """
        self._conn = sql.connect(self._sqlite_file)
        try:
            yield self._conn
        finally:
            self._conn.close()

    #
    def clear_input(self):
        """Load params from SQL and initialize other entities to default value."""

        if self._app.insight.test_mode:
            self._warn_about_work_dir()
            if self._does_db_exist():
                print('Test mode: Loading parameters from data repository in: "{}".\n'
                      'Test mode: Setting uninitialized scalars to default value.\n'
                      .format(self._app.insight.work_dir))
                with self._connect():
                    self._load_params_and_meta()
                    self._init_default_values(xi_types.Scalar)

                #
                self._clean_db()

                with self._connect():
                    self._save_params()
            else:
                print('Test mode: Creating new data repository in: "{}".\n'
                      'Test mode: Setting uninitialized parameters and scalars to default value.\n'
                      .format(self._app.insight.work_dir))
                self._clean_db()
                with self._connect():
                    self._init_default_values(xi_types.Param)
                    self._init_default_values(xi_types.Scalar)
                    self._save_params()
        else:
            self._check_db_exists()
            with self._connect():
                self._load_params_and_meta()
                self._init_default_values(xi_types.Scalar)

    #
    def save_input(self):
        with self._connect():
            self._save_scalars(xi_types.Manage.INPUT)
            self._save(manage=xi_types.Manage.INPUT)

    #
    def load_input(self):
        if self._app.insight.test_mode:
            self._warn_about_work_dir()
            if self._does_db_exist():
                print('Test mode: Loading parameters and input from data repository in: "{}".\n'
                      .format(self._app.insight.work_dir))
                with self._connect():
                    self._load_params_and_meta()
                    self._load_scalars(manage=xi_types.Manage.INPUT)
                    self._load(manage=xi_types.Manage.INPUT)
                    #
                    self._init_default_values(xi_types.Scalar)
            else:
                print('Test mode: Creating new data repository in: "{}".\n'
                      'Test mode: Setting uninitialized parameters and scalars to default value.\n'
                      'Test mode: Inputs have to be initialized manually before calling this execution mode.\n'
                      .format(self._app.insight.work_dir))
                self._clean_db()
                with self._connect():
                    self._init_default_values(xi_types.Param)
                    self._init_default_values(xi_types.Scalar)
                    self.save_input()
        else:
            self._check_db_exists()
            with self._connect():
                self._load_params_and_meta()
                self._load_scalars(manage=xi_types.Manage.INPUT)
                self._load(manage=xi_types.Manage.INPUT)
                #
                self._init_default_values(xi_types.Scalar)

    #
    def save_result(self):
        with self._connect():
            self._save_scalars(manage=xi_types.Manage.RESULT)
            self._save(manage=xi_types.Manage.RESULT)


class SQLiteConnector(Sqlite3Connector):
    def __init__(self, app):
        super().__init__(app, os.path.join(app.insight.work_dir, SQLITE_FILENAME))
