from __future__ import annotations

from typing import Dict, List

from ..data._base import NOT_GIVEN, filter_not_given, maybe_to_dict
from ..data.chat import ChatMessage
from ..data.model import Model, ModelOutput
from ._resource import APIResource


def _maybe_headers_to_list(headers: Dict[str, str] | None):
    if isinstance(headers, dict):
        return [{"name": k, "value": v} for k, v in headers.items()]
    return headers if headers is not None else []


class ModelsResource(APIResource):
    def retrieve(self, model_id: str) -> Model:
        return self._client.get(f"/models/{model_id}", cast_to=Model)

    def create(
        self,
        *,
        name: str,
        description: str,
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
        return self._client.post(
            "/models",
            json=data,
            cast_to=Model,
        )

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
        return self._client.patch(
            f"/models/{model_id}",
            json=data,
            cast_to=Model,
        )

    def delete(self, model_id: str | List[str]) -> None:
        self._client.delete("/models", params={"model_ids": model_id})

    def list(self, project_id: str) -> List[Model]:
        return self._client.get(
            "/models", params={"project_id": project_id}, cast_to=Model
        )

    def chat(self, model_id: str, messages: List[ChatMessage]) -> ModelOutput:
        return self._client.post(
            f"/models/{model_id}/chat",
            json={"messages": [maybe_to_dict(msg) for msg in messages]},
            cast_to=ModelOutput,
        )
