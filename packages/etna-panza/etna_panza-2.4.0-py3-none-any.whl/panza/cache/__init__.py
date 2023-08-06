"""
Module providing cache-management utilities
"""

from collections import OrderedDict
from contextlib import contextmanager
import os
import shutil


class Cache:
    """
    Class managing a simple file-based cache, meant to be used by a single owner
    """

    def __init__(self, path: str, max_entries: int):
        self.cache_root = path
        self.max_entries = max_entries
        self.entries = OrderedDict()

    def __repr__(self) -> str:
        return f"Cache(path={self.cache_root}, max_entries={self.max_entries})"

    def _entry_path(self, name: str) -> str:
        return os.path.join(self.cache_root, name)

    def _remove_entry(self, name: str):
        entry_path = self._entry_path(name)
        shutil.rmtree(entry_path, ignore_errors=True)

    def remove_entry(self, name: str):
        if self.has_entry(name):
            self._remove_entry(name)

    @contextmanager
    def add_entry(self, name: str) -> str:
        entry_path = self._entry_path(name)
        if self.has_entry(name):
            self.entries.move_to_end(name)
        else:
            if len(self.entries) == self.max_entries:
                evicted, _ = self.entries.popitem(last=False)
                self._remove_entry(evicted)
            os.makedirs(entry_path, mode=0o775)
            self.entries[name] = None
        try:
            yield entry_path
        finally:
            pass

    def get_entry(self, name: str) -> str:
        if not self.has_entry(name):
            raise FileNotFoundError(name)
        self.entries.move_to_end(name)
        return self._entry_path(name)

    def has_entry(self, name: str) -> bool:
        return name in self.entries

    def remove(self, ignore_errors=True):
        """Delete cache_root and its content recursively."""
        shutil.rmtree(self.cache_root, ignore_errors=ignore_errors)

    @staticmethod
    def from_directory(path: str, *, max_entries: int) -> 'Cache':
        return Cache(path, max_entries)

    @staticmethod
    def create_at(path: str, *, max_entries: int, exist_ok=False) -> 'Cache':
        os.makedirs(path, mode=0o775, exist_ok=exist_ok)
        return Cache.from_directory(path, max_entries=max_entries)
