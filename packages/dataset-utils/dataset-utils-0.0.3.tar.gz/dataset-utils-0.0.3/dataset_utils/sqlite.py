import dataset
from dataset.types import Types
from enum import Enum
from urllib.parse import urlparse
from sqlalchemy import event
import sqlite3
import os
from dataset.database import Database


class ConnectMode(Enum):
    # Rollback journal (the default mode)
    JOURNAL = 1
    # Write-Ahead-Log:
    # https://www.sqlite.org/wal.html
    WAL = 2
    READ_ONLY = 3


def connect(path, mode=ConnectMode.JOURNAL, ensure_exists=False):
    # NOTE: if you open in read-only mode, we always check to see it exists
    # otherwise, if ensure_exists is False, we might create it if it doesn't exist
    if ensure_exists:
        assert os.path.exists(path)
    if mode == ConnectMode.JOURNAL:
        return connect_journal(path)
    elif mode == ConnectMode.WAL:
        return connect_wal(path)
    else:
        assert mode == ConnectMode.READ_ONLY
        return connect_ro(path)


def connect_journal(path):
    return dataset.connect('sqlite:///' + path)


def connect_ro(path):
    # https://github.com/pudo/dataset/issues/136
    # https://stackoverflow.com/questions/27910829/sqlalchemy-and-sqlite-shared-cache
    assert os.path.exists(path)
    creator = lambda: sqlite3.connect('file:' + path + '?mode=ro', uri=True)
    return dataset.connect('sqlite:///', engine_kwargs={'creator': creator})


def connect_wal(path) -> dataset.Database:
    assert not path.startswith('sqlite:')
    url = 'sqlite:///' + path
    parsed_url = urlparse(url)

    db = dataset.connect(url)

    def _enable_sqlite_wal_mode(dbapi_con, con_record):
        # reference:
        # https://stackoverflow.com/questions/9671490/how-to-set-sqlite-pragma-statements-with-sqlalchemy
        # https://stackoverflow.com/a/7831210/1890086
        dbapi_con.execute("PRAGMA journal_mode=WAL")

    assert parsed_url.scheme.lower() == 'sqlite' and parsed_url.path != ''
    # we only enable WAL mode for sqlite databases that are not in-memory
    event.listen(db.engine, 'connect', _enable_sqlite_wal_mode)
    return db


def get_or_create(path_or_db, table_name, mode=ConnectMode.JOURNAL, primary_id=None, columns=None, types=None, index=None):
    # by default, types are all string (text or string - they're the same in sqlite)
    # more readable than calling get_or_create_from_dict
    generated_dict = {}
    if types is None:
        types = dict()
    if columns is not None:
        assert isinstance(columns, list) or isinstance(columns, tuple)
    def get_type(column, default='text'):
        type_ = types.get(column)
        if type_ is None:
            type_ = default
        return getattr(dataset.types.Types, type_)

    if primary_id:
        generated_dict['primary'] = (primary_id, get_type(primary_id))
    generated_dict['columns'] = []
    if columns:
        for column in columns:
            generated_dict['columns'].append((column, get_type(column)))
    if index:
        generated_dict['index'] = index

    db = get_or_create_from_dict(path_or_db, {table_name: generated_dict}, mode=mode)
    return db, db[table_name]


def get_or_create_from_dict(path_or_db, table_info: dict, mode=ConnectMode.JOURNAL) -> dataset.Database:
    if not isinstance(path_or_db, dataset.Database):
        assert isinstance(path_or_db, str)
        db = connect(path_or_db, mode)
    else:
        db = path_or_db

    def get_type(type_):
        if isinstance(type_, str):
            return getattr(db.types, type_)
        return type_

    for table_name in table_info.keys():
        ct = table_info[table_name]
        if table_name not in db:
            # create column if it doesn't exist
            # Create table_name
            assert 'primary' in ct
            assert 'columns' in ct
            if 'primary' in ct:
                primary_id, primary_key = ct['primary']
                table = db.create_table(table_name, primary_id=primary_id, primary_type=get_type(primary_key))
            else:
                table = db.create_table(table_name)
        else:
            table = db[table_name]
        assert isinstance(table, dataset.Table)
        assert isinstance(ct['columns'], list)
        for col in ct['columns']:
            col_name, col_type = col
            if not table.has_column(col_name):
                table.create_column(col_name, get_type(col_type))
        if 'index' in ct:
            for cc in ct['index']:
                idxcols = cc
                if not isinstance(cc, list):
                    idxcols = [cc]
                if not table.has_index(idxcols):
                    table.create_index(idxcols)
    return db


class RamCache():
    # TODO - in the middle of implementing

    @classmethod
    def from_path(cls, path):
        pass

    # For now, read-only
    def __init__(self, path, cache_dir='/dev/shm/'):
        assert os.path.isdir(cache_dir)
        assert os.path.exists(path)
        import shutil
        shutil.copy(path, cache_dir)
        from pathlib import Path
        self.cached_path = os.path.join(cache_dir, Path(path).name)
        assert os.path.isfile(self.cached_path)
        self.db = connect_ro(self.cached_path)
        self.closed = False

    def close(self):
        self.closed = True
        import shutil
        os.remove(self.cached_path)

