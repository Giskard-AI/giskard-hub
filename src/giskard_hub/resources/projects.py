from __future__ import annotations

from typing import List, Optional

from ..data._base import NOT_GIVEN, filter_not_given, maybe_to_dict
from ..data.project import FailureCategory, Project
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
        failure_categories: Optional[List[FailureCategory]] = NOT_GIVEN,
    ):
        if failure_categories is not NOT_GIVEN:
            failure_categories = maybe_to_dict(failure_categories)

        data = filter_not_given(
            {
                "name": name,
                "description": description,
                "failure_categories": failure_categories,
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
        data = self._client.get("/projects")
        return [Project.from_dict(item, _client=self._client) for item in data]
