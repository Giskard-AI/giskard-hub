from __future__ import annotations

from typing import List, Union

from ..data._base import NOT_GIVEN, NotGiven, filter_not_given
from ..data.knowledge_base import Document, KnowledgeBase, Topic
from ._resource import APIResource


class KnowledgeBasesResource(APIResource):
    """Resource for managing knowledge bases."""

    def retrieve(self, knowledge_base_id: str) -> KnowledgeBase:
        """Retrieve a knowledge base by ID."""
        return self._client.get(
            f"/knowledge-bases/{knowledge_base_id}",
            cast_to=KnowledgeBase,
        )

    def create(
        self,
        *,
        project_id: str,
        name: str,
        filename: str,
        description: Union[str, NotGiven] = NOT_GIVEN,
        document_column: Union[str, NotGiven] = NOT_GIVEN,
        topic_column: Union[str, NotGiven] = NOT_GIVEN,
    ) -> KnowledgeBase:
        """Create a new knowledge base."""
        # Prepare multipart/form-data body with kb_file and other fields as query params
        params = filter_not_given(
            {
                "project_id": project_id,
                "name": name,
                "description": description,
                "document_column": document_column,
                "topic_column": topic_column,
            }
        )

        # Open file and pass the file handle directly
        with open(filename, "rb") as fp:
            print(params)

            return self._client.post(
                "/knowledge-bases",
                params=params,
                files={"kb_file": (str(filename), fp, "application/jsonl")},
                cast_to=KnowledgeBase,
            )

    def update(
        self,
        knowledge_base_id: str,
        *,
        name: Union[str, NotGiven] = NOT_GIVEN,
        description: Union[str, NotGiven] = NOT_GIVEN,
        project_id: Union[str, NotGiven] = NOT_GIVEN,
    ) -> KnowledgeBase:
        """Update a knowledge base."""
        data = filter_not_given(
            {
                "name": name,
                "description": description,
                "project_id": project_id,
            }
        )
        return self._client.patch(
            f"/knowledge-bases/{knowledge_base_id}",
            json=data,
            cast_to=KnowledgeBase,
        )

    def delete(self, knowledge_base_id: str | List[str]) -> None:
        """Delete one or more knowledge bases."""
        if isinstance(knowledge_base_id, str):
            knowledge_base_id = [knowledge_base_id]
        self._client.delete(
            "/knowledge-bases", params={"knowledge_base_ids": knowledge_base_id}
        )

    def list(self, project_id: str) -> List[KnowledgeBase]:
        """List knowledge bases, filtered by project."""
        params = {"project_id": project_id}
        return self._client.get(
            "/knowledge-bases",
            params=params,
            cast_to=KnowledgeBase,
        )

    def list_topics(self, knowledge_base_id: str) -> List[Topic]:
        """List topics for a knowledge base."""
        return self._client.get(
            f"/knowledge-bases/{knowledge_base_id}/topics",
            cast_to=Topic,
        )

    def list_documents(
        self, knowledge_base_id: str, topic_id: Union[str, NotGiven] = NOT_GIVEN
    ) -> List[Document]:
        """List documents for a knowledge base, optionally filtered by topic."""
        params = filter_not_given({"topic_id": topic_id})
        return self._client.get(
            f"/knowledge-bases/{knowledge_base_id}/documents",
            params=params,
            cast_to=Document,
        )
