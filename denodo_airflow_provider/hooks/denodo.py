# Adapted from airflow/providers/postgres/hooks/postgres.py
# licensed under the Apache License, Version 2.0 (the "License");
from typing import Iterable, Any

from airflow.providers.common.sql.hooks.sql import DbApiHook
from psycopg2._psycopg import connection
from sqlalchemy.engine import URL

from copy import deepcopy
import psycopg2
import psycopg2.extensions
import psycopg2.extras

class DenodoHook(DbApiHook):
    conn_name_attr = "denodo_conn_id"
    default_conn_name = "denodo_default"
    conn_type = "denodo"
    hook_name = "denodo"
    supports_autocommit = True
    supports_executemany = True


    def __init__(
        self, *args, options: str | None = None, enable_log_db_messages: bool = False, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.conn: connection = None
        self.database: str | None = kwargs.pop("database", None)
        self.options = options
        self.enable_log_db_messages = enable_log_db_messages


    @property
    def sqlalchemy_url(self) -> URL:
        conn = self.get_connection(self.get_conn_id())
        return URL.create(
            drivername="denodo+psycopg2",
            username=conn.login,
            password=conn.password,
            host=conn.host,
            port=conn.port,
            database=self.database or conn.schema,
        )


    def get_uri(self) -> str:
        """
        Extract the URI from the connection.

        :return: the extracted URI in Sqlalchemy URI format.
        """
        return self.sqlalchemy_url.render_as_string(hide_password=False)


    def _get_cursor(self, raw_cursor: str):
        _cursor = raw_cursor.lower()
        cursor_types = {
            "dictcursor": psycopg2.extras.DictCursor,
            "realdictcursor": psycopg2.extras.RealDictCursor,
            "namedtuplecursor": psycopg2.extras.NamedTupleCursor,
        }
        if _cursor in cursor_types:
            return cursor_types[_cursor]
        else:
            valid_cursors = ", ".join(cursor_types.keys())
            raise ValueError(f"Invalid cursor passed {_cursor}. Valid options are: {valid_cursors}")

    def get_conn(self) -> connection:
        """Establish a connection to a database."""
        conn = deepcopy(self.connection)

        conn_args = {
            "host": conn.host,
            "user": conn.login,
            "password": conn.password,
            "dbname": self.database or conn.schema,
            "port": conn.port,
        }
        raw_cursor = conn.extra_dejson.get("cursor", False)
        if raw_cursor:
            conn_args["cursor_factory"] = self._get_cursor(raw_cursor)

        if self.options:
            conn_args["options"] = self.options

        for arg_name, arg_val in conn.extra_dejson.items():
            if arg_name not in [
                "cursor",
            ]:
                conn_args[arg_name] = arg_val

        self.conn = psycopg2.connect(**conn_args)
        return self.conn


    @staticmethod
    def _serialize_cell(cell: object, conn: connection | None = None) -> Any:
        """
        Serialize a cell.

        psycopg2 adapts all arguments to the ``execute()`` method internally,
        hence we return the cell without any conversion.

        See http://initd.org/psycopg/docs/advanced.html#adapting-new-types for
        more information.

        :param cell: The cell to insert into the table
        :param conn: The database connection
        :return: The cell
        """
        return cell

    def get_openlineage_database_info(self, connection):
        authority = DbApiHook.get_openlineage_authority_part(  # type: ignore[attr-defined]
            connection, default_port=9996
        )

        return dict(
            scheme="denodo",
            authority=authority,
            database=self.database or connection.schema,
        )

    def get_openlineage_database_dialect(self, connection) -> str:
        return "denodo"

    def get_openlineage_default_schema(self) -> str | None:
        return ""

    @classmethod
    def get_ui_field_behaviour(cls) -> dict[str, Any]:
        return {
            "hidden_fields": [],
            "relabeling": {
                "schema": "Database",
            },
        }

    def get_db_log_messages(self, conn) -> None:
        """
        Log all database messages sent to the client during the session.

        :param conn: Connection object
        """
        pass
