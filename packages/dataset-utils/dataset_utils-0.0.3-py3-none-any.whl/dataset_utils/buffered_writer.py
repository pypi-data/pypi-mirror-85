"""
This is similar to the chunked writer:
https://github.com/pudo/dataset/blob/master/dataset/chunked.py
Except it:
- has multiple other conflict resolution modes
- checks to see if the inserted row is in the buffer
"""
import time
from enum import Enum
from threading import RLock


class ConflictChecker(Enum):
    # Don't check to see if there are conflicts. Similar to bulk insert
    DONT_CHECK = 1
    # If a row exists, don't replace it
    KEEP_EXISTING = 2
    # If a row exists, overwrite it
    OVERWRITE = 3


class BufferedTableWriter(object):

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.force_flush()

    def __init__(self, table, key_column=None, flush_every=5, flush_after_size=1000,
                 key_conflicts=ConflictChecker.DONT_CHECK):
        self.table = table
        self.key_column = key_column
        self.queue = []
        self.last_flushed = 0
        self.flush_every = flush_every
        self.flush_after_size = flush_after_size
        self.key_conflicts = key_conflicts
        self.insert_lock = RLock()

    def _row_exists(self, key_):
        id_dict = {
            self.key_column: key_,
        }
        return self.table.find_one(**id_dict) is not None

    def insert(self, row: dict, key_=None):
        should_insert = True
        if self.key_conflicts == ConflictChecker.DONT_CHECK:
            # don't do any checks
            pass
        elif self.key_conflicts == ConflictChecker.KEEP_EXISTING:
            assert self.key_column is not None
            assert key_ is not None
            with self.insert_lock:
                exists = self._row_exists(key_)
                if exists:
                    should_insert = False
                # Check the rest of the queue as well
                for e in self.queue:
                    if e[self.key_column] == key_:
                        should_insert = False
        elif self.key_conflicts == ConflictChecker.OVERWRITE:
            assert self.key_column is not None
            assert key_ is not None
            with self.insert_lock:
                # Check the rest of the queue as well
                del_idx = None
                for idx, e in enumerate(self.queue):
                    if e[self.key_column] == key_:
                        del_idx = idx
                if del_idx is not None:
                    del self.queue[del_idx]
        else:
            raise Exception('error: unhandled key conflicts state')
        if should_insert:
            self.queue.append(row)
        self.lazy_flush()

    def lazy_flush(self):
        should_flush = False
        if (time.time() - self.last_flushed) > self.flush_every:
            should_flush = True
        if len(self.queue) > self.flush_after_size:
            should_flush = True
        if should_flush:
            self.force_flush()

    def force_flush(self):
        self.last_flushed = time.time()
        if len(self.queue) > 0:
            self.table.insert_many(self.queue)
            self.queue = []

