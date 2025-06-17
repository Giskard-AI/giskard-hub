from typing import Any, Dict, List, Optional

from ..data._base import NOT_GIVEN, filter_not_given
from ..data.check import Check, extract_check_params
from ._resource import APIResource


class ChecksResource(APIResource):
    def list(self, project_id: str):
        data = self._client.get(
            "/checks",
            params={"project_id": project_id, "filter_builtin": True},
        )

        return [
            Check.from_dict(
                {
                    **check,
                    "params": extract_check_params(check),
                }
            )
            for check in data
        ]

    def retrieve(self, check_id: str):
        data = self._client.get(f"/checks/{check_id}")
        return Check.from_dict(
            {
                **data,
                "params": extract_check_params(data),
            }
        )

    def delete(self, check_id: str | List[str]) -> None:
        return self._client.delete("/checks", params={"check_ids": check_id})

    def create(
        self,
        *,
        project_id: str,
        identifier: str,
        name: str,
        params: Dict[str, Any],
        description: Optional[str] = None,
    ) -> Check:
        data = self._client.post(
            "/checks",
            json={
                "project_id": project_id,
                "description": description,
                "name": name,
                "identifier": identifier,
                "assertions": [params],
            },
        )
        return Check.from_dict({**data, "params": extract_check_params(data)})

    def update(
        self,
        check_id: str,
        *,
        identifier: Optional[str] = NOT_GIVEN,
        name: Optional[str] = NOT_GIVEN,
        description: Optional[str] = NOT_GIVEN,
        params: Optional[Dict[str, Any]] = NOT_GIVEN,
    ) -> Check:

        data = filter_not_given(
            {
                "identifier": identifier,
                "name": name,
                "description": description,
                "assertions": [params] if params != NOT_GIVEN else NOT_GIVEN,
            }
        )

        data = self._client.patch(f"/checks/{check_id}", json=data)
        return Check.from_dict({**data, "params": extract_check_params(data)})
