from __future__ import annotations

from typing import Optional

import httpx

_default_http_client_kwargs = {
    "follow_redirects": True,
    "timeout": httpx.Timeout(30.0),
}


class SyncClient:
    _http: httpx.Client

    def __init__(self, *, http_client: Optional[httpx.Client] = None):
        self._http = http_client or httpx.Client(**_default_http_client_kwargs)

    def _headers(self):
        return {}

    def _request(self, method: str, path: str, *, cast_to=None, **kwargs):
        res = self._http.request(
            method=method,
            url=path,
            headers=self._headers(),
            **kwargs,
        )
        try:
            res.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == httpx.codes.UNPROCESSABLE_ENTITY:
                raise ValueError("Validation error: " + e.response.text)

            try:
                detail = e.response.json()
                raise httpx.HTTPStatusError(
                    message="API Error: " + detail.get("detail", e.response.text),
                    request=e.request,
                    response=e.response,
                )
            except TypeError:
                pass

            raise e
        data = res.json()

        if cast_to:
            data = self._cast_data_to(cast_to, data)

        return data

    def get(self, path: str, **kwargs):
        return self._request("GET", path, **kwargs)

    def post(self, path: str, **kwargs):
        return self._request("POST", path, **kwargs)

    def patch(self, path: str, **kwargs):
        return self._request("PATCH", path, **kwargs)

    def put(self, path: str, **kwargs):
        return self._request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs):
        return self._request("DELETE", path, **kwargs)

    def close(self):
        try:
            self._http.close()
        except AttributeError:
            # This may happen if the client was not properly initialized yet
            pass

    def __del__(self):
        self.close()

    def _cast_data_to(self, cast_to, data):
        if isinstance(data, list):
            return [cast_to.from_dict(d, _client=self) for d in data]

        return cast_to.from_dict(data, _client=self)
