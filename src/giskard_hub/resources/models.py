from __future__ import annotations

from typing import Dict, List, Optional

from ..data._base import NOT_GIVEN, filter_not_given, maybe_to_dict
from ..data.chat import ChatMessage
from ..data.model import Model, ModelOutput
from ._resource import APIResource


def _maybe_headers_to_list(headers: Dict[str, str] | None):
    if isinstance(headers, dict):
        return [{"name": k, "value": v} for k, v in headers.items()]
    return headers if headers is not None else []


class ModelsResource(APIResource):
    _base_url = "/v2/models"

    def retrieve(self, model_id: str) -> Model:
        response = self._client.get(f"{self._base_url}/{model_id}")
        return Model.from_dict(response["data"], _client=self._client)

    # pylint: disable=too-many-arguments
    def create(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        url: str,
        supported_languages: List[str],
        headers: Dict[str, str] = None,
        project_id: str,
    ) -> Model:
        data = filter_not_given(
            {
                "name": name,
                "description": description,
                "url": url,
                "supported_languages": supported_languages,
                "headers": _maybe_headers_to_list(headers),
                "project_id": project_id,
            }
        )

        response = self._client.post(
            self._base_url,
            json=data,
        )

        return Model.from_dict(response["data"], _client=self._client)

    # pylint: disable=too-many-arguments
    def update(
        self,
        model_id: str,
        *,
        name: str = NOT_GIVEN,
        description: str = NOT_GIVEN,
        url: str = NOT_GIVEN,
        supported_languages: List[str] = NOT_GIVEN,
        headers: Dict[str, str] = NOT_GIVEN,
        project_id: str = NOT_GIVEN,
    ) -> Model:
        data = filter_not_given(
            {
                "name": name,
                "description": description,
                "url": url,
                "supported_languages": supported_languages,
                "headers": _maybe_headers_to_list(headers),
                "project_id": project_id,
            }
        )

        response = self._client.patch(
            f"{self._base_url}/{model_id}",
            json=data,
        )

        return Model.from_dict(response["data"], _client=self._client)

    def delete(self, model_id: str | List[str]) -> None:
        if isinstance(model_id, str):
            self._client.delete(f"{self._base_url}/{model_id}")
            return
        self._client.delete(self._base_url, params={"model_ids": model_id})

    def list(self, project_id: str) -> List[Model]:
        response = self._client.get(self._base_url, params={"project_id": project_id})

        return [
            Model.from_dict(item, _client=self._client) for item in response["data"]
        ]

    def chat(self, model_id: str, messages: List[ChatMessage]) -> ModelOutput:
        response = self._client.post(
            f"{self._base_url}/{model_id}/completions",
            json={"messages": [maybe_to_dict(msg) for msg in messages]},
        )

        return ModelOutput.from_dict(response["data"], _client=self._client)
