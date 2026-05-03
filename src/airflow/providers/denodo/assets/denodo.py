# Adapted from https://github.com/apache/airflow/blob/3.2.1/providers/postgres/src/airflow/providers/postgres/assets/postgres.py

from urllib.parse import SplitResult

def sanitize_uri(uri: SplitResult) -> SplitResult:
    if not uri.netloc:
        raise ValueError("URI format denodo:// must contain a host")
    if uri.port is None:
        host = uri.netloc.rstrip(":")
        uri = uri._replace(netloc=f"{host}:9996")
    path_parts = uri.path.split("/")
    if len(path_parts) != 3:  # Leading slash, database, and table names.
        raise ValueError("URI format denodo:// must contain database and table names")
    return uri._replace(scheme="denodo", path="/".join(path_parts))