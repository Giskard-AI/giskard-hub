from __future__ import annotations

from typing import List

from ..data._base import NOT_GIVEN, filter_not_given
from ..data.project import Project
from ._resource import APIResource


class ProjectsResource(APIResource):
    def retrieve(self, project_id: str):
        return self._client.get(f"/projects/{project_id}", cast_to=Project)

    def create(
        self,
        *,
        name: str,
        description: str = "",
    ):
        data = filter_not_given(
            {
                "name": name,
                "description": description,
            }
        )
        return self._client.post(
            "/projects",
            json=data,
            cast_to=Project,
        )

    def update(
        self,
        project_id: str,
        *,
        name: str = NOT_GIVEN,
        description: str = NOT_GIVEN,
    ):
        data = filter_not_given(
            {
                "name": name,
                "description": description,
            }
        )
        return self._client.patch(
            f"/projects/{project_id}",
            json=data,
            cast_to=Project,
        )

    def delete(self, project_id: str | List[str]):
        return self._client.delete("/projects", params={"project_ids": project_id})

    def list(self):
        return self._client.get("/projects", cast_to=Project)
