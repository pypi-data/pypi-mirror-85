from contextlib import contextmanager
from posixpath import join as url_join

from gcsfs.core import GCSFileSystem
from google.oauth2.service_account import Credentials

from emporium.base import AbstractStore, Entry


class RemoteStoreGCS(AbstractStore):

    DEFAULT_URL = "https://storage.googleapis.com/storage/v1/b/{bucket}/o/{path}"
    SCOPES = ["https://www.googleapis.com/auth/devstorage.read_write"]

    # pylint: disable=too-many-arguments
    def __init__(
        self, bucket, prefix=None, project=None, token=None, url=None, **extra
    ):
        """Instantiate a store that puts data on Google Cloud Storage.

        :param bucket: The bucket to store data in. It needs to exist already.
        :param prefix: The prefix (e.g. path) within that bucket
        :param project: The name of the project to which the bucket belongs.
        :param token: The token, see
            https://gcsfs.readthedocs.io/en/latest/index.html, for options.
        :param url: The URL pattern that external clients can use to refer to an
            object in the store. Should have placeholders ``{bucket}`` and ``{path}``.
        """
        self._bucket = bucket
        self._prefix = None if not prefix else prefix.lstrip("/")
        if project is None and isinstance(token, dict):
            # Parameter 'token' holds an account info dict
            self._project = token.get("project") or token.get("project_id")
        else:
            self._project = project
        self._token = token
        self._url = url or self.DEFAULT_URL
        # To be able to create substores on the same file system.
        self.__fs = extra.pop("_fs", None)
        self._extra = extra

    @classmethod
    def from_config(cls, config):
        return cls(**config)

    @property
    def _fs(self):
        if self.__fs is None:
            if isinstance(self._token, dict):
                # Convert to credentials, as directly passing in the account
                # info does not seem to work.
                token = Credentials.from_service_account_info(
                    self._token, scopes=self.SCOPES
                )
            else:
                token = self._token
            self.__fs = GCSFileSystem(project=self._project, token=token, **self._extra)
        return self.__fs

    @contextmanager
    def open(self, path, mode, *args, **kwargs):
        segments = [self._bucket, self._prefix, path.lstrip("/")]
        path = url_join(*(s for s in segments if s))
        with self._fs.open(path, mode, *args, **kwargs) as h:
            yield h

    def substore(self, path):
        path = path.lstrip("/")
        subpath = url_join(self._prefix, path) if self._prefix is not None else path
        cls = self.__class__
        return cls(self._bucket, subpath, self._project, self._token, self._url, _fs=self.__fs)

    def location(self, path=None):
        segments = [s.lstrip("/") for s in [self._prefix, path] if s]
        if segments:
            return self._url.format(bucket=self._bucket, path=url_join(*segments))
        return self._url.format(bucket=self._bucket, path="")

    def list(self, path=None):
        segments = [self._bucket, self._prefix, (path or "").lstrip("/")]
        path = url_join(*(s for s in segments if s))
        for file_name in self._fs.ls(path):
            if self._fs.isdir(file_name):
                yield Entry(file_name.split("/")[-1], "directory")
            else:
                yield Entry(file_name.split("/")[-1], "file")
