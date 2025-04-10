from __future__ import annotations

import json
from typing import Optional, Tuple

import httpx

from .errors import (
    HubAPIError,
    HubAuthenticationError,
    HubForbiddenError,
    HubJSONDecodeError,
    HubValidationError,
)

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

    def _extract_error_message(self, response: httpx.Response, default_msg: str) -> str:
        """Extract error message from response, falling back to default_msg if not found"""
        try:
            error_data = response.json()
            if "message" in error_data:
                return error_data["message"]
        except json.JSONDecodeError:
            pass
        return default_msg

    def _extract_validation_errors(self, response: httpx.Response) -> Tuple[str, str]:
        """Extract validation error message and field errors from response"""
        error_message = "Validation error. Please check your request."
        fields_str = ""

        try:
            error_data = response.json()
            if "message" in error_data:
                error_message = error_data["message"]
            if "fields" in error_data:
                fields_str = str(error_data["fields"])
        except json.JSONDecodeError:
            pass

        return error_message, fields_str

    def _request(self, method: str, path: str, *, cast_to=None, **kwargs):
        try:
            res = self._http.request(
                method=method,
                url=path,
                headers=self._headers(),
                **kwargs,
            )

            # Handle authentication errors
            if res.status_code == 401:
                raise HubAuthenticationError(
                    "Authentication failed. Please check your API key.",
                    status_code=res.status_code,
                    response_text=res.text,
                )

            # Handle forbidden errors
            if res.status_code == 403:
                error_message = self._extract_error_message(
                    res, "You don't have permission to access this resource."
                )
                raise HubForbiddenError(
                    error_message,
                    status_code=res.status_code,
                    response_text=res.text,
                )

            # Handle validation errors
            if res.status_code == 422:
                error_message, fields_str = self._extract_validation_errors(res)
                if fields_str:
                    error_message = f"{error_message}\n{fields_str}"

                raise HubValidationError(
                    error_message,
                    status_code=res.status_code,
                    response_text=res.text,
                )

            # Handle other HTTP errors
            try:
                res.raise_for_status()
            except httpx.HTTPStatusError as e:
                error_message = self._extract_error_message(e.response, e.response.text)
                raise HubAPIError(
                    error_message,
                    status_code=e.response.status_code,
                    response_text=e.response.text,
                ) from e

            # Parse response JSON
            try:
                data = res.json()
            except json.JSONDecodeError as e:
                raise HubJSONDecodeError(
                    f"Failed to decode API response as JSON: {str(e)}",
                    status_code=res.status_code,
                    response_text=res.text,
                ) from e

            if cast_to:
                data = self._cast_data_to(cast_to, data)

            return data

        except HubAPIError:
            raise
        except Exception as e:
            raise HubAPIError(
                f"Unexpected error while making API request: {str(e)}",
                response_text=str(e),
            ) from e

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
