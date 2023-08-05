import os
import io
from contextlib import contextmanager
from posixpath import join as url_join

from emporium.base import AbstractStore, Entry
from emporium.utils import is_write_mode


class InMemoryStore(AbstractStore):
    """Store that keeps data in memory."""

    def __init__(self, data=None, prefix=None):
        """Instantiate a store.

        :returns: Instance that implements :class:`~emporium.base.AbstractStore`.
        """
        self._data = data if data is not None else {}
        self._prefix = prefix or ""

    @classmethod
    def from_config(cls, config):
        # pylint: disable=unused-argument
        return cls()

    @contextmanager
    def open(self, path, mode, *args, **kwargs):
        path = url_join(self._prefix, path.lstrip("/"))

        if is_write_mode(mode):
            if mode in ["w", "wt"]:
                resource = io.StringIO()
                yield resource
                resource.seek(0)
                self._data[path] = resource.read().encode("utf-8")
            if mode in ["wb"]:
                resource = io.BytesIO()
                yield resource
                resource.seek(0)
                self._data[path] = resource.read()

        if path not in self._data:
            raise FileNotFoundError()
        if mode in ["r", "rt"]:
            yield io.StringIO(self._data[path].decode("utf-8"))
        if mode in ["rb"]:
            yield io.BytesIO(self._data[path])

    def substore(self, path):
        return self.__class__(data=self._data, prefix=path)

    def location(self, path):
        return path

    def list(self, path=None):
        segments = [s for s in [self._prefix, path] if s is not None]
        if segments:
            prefix = url_join(*segments)
        else:
            prefix = None
        seen = set()
        for entry in list(self._data.keys()):
            relative_entry = os.path.relpath(entry, prefix)
            if len(relative_entry.split(os.sep)) > 1 or entry.endswith(os.sep):
                entry_tuple = Entry(relative_entry.split(os.sep)[0], "directory")
            else:
                entry_tuple = Entry(relative_entry.split(os.sep)[0], "file")
            if entry_tuple not in seen:
                yield entry_tuple
                seen.add(entry_tuple)

    def read_raw(self, path):
        return self._data.get(path)

    def write_raw(self, path, contents):
        self._data[path] = contents

    def __repr__(self):
        return "<{}({})>".format(self.__class__.__name__, self._prefix)
