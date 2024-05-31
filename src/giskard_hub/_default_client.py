_client = None


def _load_client():
    global _client
    if _client is None:
        from giskard_hub import hub_url, api_key
        from giskard_hub.client import HubClient

        _client = HubClient(hub_url=hub_url, api_key=api_key)

    return _client
