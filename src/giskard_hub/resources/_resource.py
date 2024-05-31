from .._base_client import SyncClient


class APIResource:
    _client: SyncClient

    def __init__(self, client: SyncClient):
        self._client = client
