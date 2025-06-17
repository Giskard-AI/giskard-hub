from typing import List

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
