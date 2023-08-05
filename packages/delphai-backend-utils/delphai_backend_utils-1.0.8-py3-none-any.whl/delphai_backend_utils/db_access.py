"""
Connection to the database
"""

from multiprocessing import current_process

import pymongo

from delphai_backend_utils.config import get_config

DB_CONN_BY_PID_AND_DBNAME = {}  # (process id, db_name) -> DB_CONN

_db_params = {
    'connection_string': get_config('db')['connection_string'],
    'default_db_name': get_config('db')['name'],
}


def get_own_db_connection(db_name: str = None) -> pymongo.database.Database:
    """
    Creates neq connection to database.
    :param db_name: use this parameter only if DB name differs from _db_params["default_db_name"]
    :return: database connection
    """
    pid = current_process().pid
    # db_config = get_config('db')
    req_db_name = _db_params['default_db_name'] if db_name is None else db_name
    if (pid, req_db_name) in DB_CONN_BY_PID_AND_DBNAME:
        return DB_CONN_BY_PID_AND_DBNAME[(pid, req_db_name)]
    client = pymongo.MongoClient(_db_params['connection_string'])

    res = client[req_db_name]
    DB_CONN_BY_PID_AND_DBNAME[(pid, req_db_name)] = res
    return res


def chunks(iterable, chunk_size=100):
    """
    Splits iterable stream by chunks of size chunk_size. Very usefull when we need to split read
    or write operations to butches of reasonable size.
    :param iterable: something interable
    :param chunk_size: desirable size if chunks to be produced
    :yield: lists of elements extracted from iterable
    """
    curr_chunk = []
    for val in iterable:
        if len(curr_chunk) >= chunk_size:
            yield curr_chunk
            curr_chunk = []
        curr_chunk.append(val)
    if curr_chunk:
        yield curr_chunk
