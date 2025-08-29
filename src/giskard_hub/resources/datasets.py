from __future__ import annotations

from typing import Any, List, Optional, Union
from uuid import UUID

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
            n_examples (int, optional): Number of examples to generate in total, regardless of the number of categories.

        Returns:
            Dataset: The generated dataset object.
        """
        payload = filter_not_given(
            {
                "model_id": model_id,
                "dataset_name": dataset_name,
                "description": description,
                "categories": categories,
                "nb_examples": n_examples,
            }
        )
        return self._client.post(
            "/datasets/generate",
            json=payload,
            cast_to=Dataset,
        )

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
        payload = filter_not_given(
            {
                "model_id": model_id,
                "knowledge_base_id": knowledge_base_id,
                "dataset_name": dataset_name,
                "description": description,
                "nb_questions": n_questions,
                "topic_ids": topic_ids,
            }
        )

        return self._client.post(
            "/datasets/generate/knowledge",
            json=payload,
            cast_to=Dataset,
        )
