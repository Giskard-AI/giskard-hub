from typing import Any, Dict, List, Optional

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
