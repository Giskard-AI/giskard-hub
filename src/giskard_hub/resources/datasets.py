from __future__ import annotations

from typing import List

from ..data._base import NOT_GIVEN, filter_not_given
from ..data.dataset import Dataset
from ._resource import APIResource


class DatasetsResource(APIResource):
    def retrieve(self, dataset_id: str):
        return self._client.get(f"/datasets/{dataset_id}", cast_to=Dataset)

    def create(self, *, name: str, description: str, project_id: str) -> Dataset:
        return self._client.post(
            "/datasets",
            json={
                "name": name,
                "description": description,
                "project_id": project_id,
            },
            cast_to=Dataset,
        )

    def update(
        self,
        dataset_id: str,
        *,
        name: str = NOT_GIVEN,
        description: str = NOT_GIVEN,
        project_id: str = NOT_GIVEN,
    ) -> Dataset:
        data = filter_not_given(
            {"name": name, "description": description, "project_id": project_id}
        )
        return self._client.patch(
            f"/datasets/{dataset_id}",
            json=data,
            cast_to=Dataset,
        )

    def delete(self, dataset_id: str | List[str]) -> None:
        self._client.delete("/datasets", params={"datasets_ids": dataset_id})

    def list(self, project_id: str) -> List[Dataset]:
        return self._client.get(
            "/datasets", params={"project_id": project_id}, cast_to=Dataset
        )
