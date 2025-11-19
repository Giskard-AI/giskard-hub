from __future__ import annotations

from typing import Any, List, Optional, Union
from uuid import UUID

from ..data._base import NOT_GIVEN, filter_not_given
from ..data.dataset import Dataset
from ._resource import APIResource


class DatasetsResource(APIResource):
    _base_url = "/v2/datasets"

    def retrieve(self, dataset_id: str):
        response = self._client.get(f"{self._base_url}/{dataset_id}")
        return Dataset.from_dict(response["data"], _client=self._client)

    def create(self, *, name: str, description: str, project_id: str) -> Dataset:
        response = self._client.post(
            self._base_url,
            json={
                "name": name,
                "description": description,
                "project_id": project_id,
            },
        )
        return Dataset.from_dict(response["data"], _client=self._client)

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
        response = self._client.patch(
            f"{self._base_url}/{dataset_id}",
            json=data,
        )
        return Dataset.from_dict(response["data"], _client=self._client)

    def delete(self, dataset_id: str | List[str]) -> None:
        if isinstance(dataset_id, str):
            self._client.delete(f"{self._base_url}/{dataset_id}")
            return
        self._client.delete(self._base_url, params={"datasets_ids": dataset_id})

    def list(self, project_id: str) -> List[Dataset]:
        response = self._client.get(self._base_url, params={"project_id": project_id})
        return [
            Dataset.from_dict(item, _client=self._client) for item in response["data"]
        ]

    def generate_adversarial(  # pylint: disable=too-many-arguments
        self,
        *,
        model_id: str,
        dataset_name: str = "Generated Dataset",
        description: str = "",
        categories: Union[List[str], Any] = NOT_GIVEN,
        n_examples: int = 10,
    ) -> Dataset:
        """
        Generate a dataset using the specified model and parameters.

        Args:
            model_id (str): The ID of the model to use for generation.
            dataset_name (str, optional): Name of the generated dataset.
            description (str, optional): Description of the dataset.
            categories (list, optional): List of issue categories, each as a dict with 'id', 'name', 'desc'.
            n_examples (int, optional): Number of examples to generate per category.

        Returns:
            Dataset: The generated dataset object.
        """
        model = self._client.get(f"/v2/models/{model_id}")
        project_id = model["data"]["project_id"]

        payload = filter_not_given(
            {
                "project_id": project_id,
                "model_id": model_id,
                "dataset_name": dataset_name,
                "description": description,
                "categories": categories,
                "n_examples_per_category": n_examples,
            }
        )
        response = self._client.post(
            f"{self._base_url}/adversarial-generations",
            json=payload,
        )
        return Dataset.from_dict(response["data"], _client=self._client)

    def generate_document_based(  # pylint: disable=too-many-arguments
        self,
        *,
        model_id: str,
        knowledge_base_id: str,
        dataset_name: str = "Generated Dataset",
        description: str = "",
        n_questions: int = 10,
        topic_ids: Optional[List[UUID]] = None,
    ) -> Dataset:
        """
        Generate a dataset from a knowledge base.

        Args:
            model_id (str): The ID of the model to use for generation.
            knowledge_base_id (str): The ID of the knowledge base.
            dataset_name (str, optional): Name of the generated dataset.
            description (str, optional): Description of the dataset.
            n_questions (int, optional): Number of questions to generate in total, regardless of the number of topics.
            topic_ids (list[UUID], optional): List of topic IDs to filter.

        Returns:
            Dataset: The generated dataset object.
        """
        if topic_ids is None:
            topic_ids = []

        model = self._client.get(f"/v2/models/{model_id}")
        project_id = model["data"]["project_id"]

        payload = filter_not_given(
            {
                "project_id": project_id,
                "model_id": model_id,
                "knowledge_base_id": knowledge_base_id,
                "dataset_name": dataset_name,
                "description": description,
                "n_examples": n_questions,
                "topic_ids": topic_ids,
            }
        )

        response = self._client.post(
            f"{self._base_url}/document-based-generations",
            json=payload,
        )
        return Dataset.from_dict(response["data"], _client=self._client)
