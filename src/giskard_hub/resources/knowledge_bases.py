from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import List, Union

from ..data._base import NOT_GIVEN, NotGiven, filter_not_given
from ..data.knowledge_base import Document, KnowledgeBase
from ._resource import APIResource


class KnowledgeBasesResource(APIResource):
    """Resource for managing knowledge bases."""

    def retrieve(self, knowledge_base_id: str) -> KnowledgeBase:
        """Retrieve a knowledge base by ID."""
        return self._client.get(
            f"/knowledge-bases/{knowledge_base_id}",
            cast_to=KnowledgeBase,
        )

    def create(  # pylint: disable=too-many-arguments
        self,
        *,
        project_id: str,
        name: str,
        data: Union[str, List[dict[str, str]]],
        description: Union[str, None] = None,
        document_column: Union[str, NotGiven] = NOT_GIVEN,
        topic_column: Union[str, NotGiven] = NOT_GIVEN,
    ) -> KnowledgeBase:
        """
        Create a new knowledge base.

        Parameters
        ----------
        project_id : str
            The project ID.
        name : str
            The name of the knowledge base.
        data : str or list[dict[str, str]]
            Either a filepath (str) to a JSON or JSONL file, or a list of dicts containing document and topic keys.
        description : str, optional
            Description of the knowledge base.
        document_column : str, optional
            Column name for document content in the data (server default is 'text').
        topic_column : str, optional
            Column name for topic classification in the data (server default is 'topic').

        Returns
        -------
        KnowledgeBase
            The created knowledge base object.
        """
        params = filter_not_given(
            {
                "project_id": project_id,
                "name": name,
                "description": description,
                "document_column": document_column,
                "topic_column": topic_column,
            }
        )

        ext = ".json"

        if isinstance(data, str):
            filepath = Path(data)
            if not filepath.exists():
                raise FileNotFoundError(f"File {filepath} not found.")
            ext = filepath.suffix.lower()
            if ext not in {".json", ".jsonl"}:
                raise ValueError(
                    "Only JSON and JSONL files are supported for file input."
                )
        elif isinstance(data, list):
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=ext, mode="w"
            ) as temp_file:
                json.dump(data, temp_file)
                filepath = Path(temp_file.name)
        else:
            raise ValueError("data must be a filepath (str) or a list of Python dicts.")

        mime_type = "application/json" if ext == ".json" else "text/jsonl"

        with filepath.open("rb") as fp:
            return self._client.post(
                "/knowledge-bases",
                params=params,
                files={"kb_file": (str(filepath.name), fp, mime_type)},
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

    def delete(self, knowledge_base_id: str | list[str]) -> None:
        """Delete one or more knowledge bases."""
        if isinstance(knowledge_base_id, str):
            knowledge_base_id = [knowledge_base_id]
        self._client.delete(
            "/knowledge-bases", params={"knowledge_base_ids": knowledge_base_id}
        )

    def list(self, project_id: str) -> list[KnowledgeBase]:
        """List knowledge bases, filtered by project."""
        params = {"project_id": project_id}
        data = self._client.get(
            "/knowledge-bases",
            params=params,
        )
        return [KnowledgeBase.from_dict(kb) for kb in data]

    def list_documents(
        self, knowledge_base_id: str, topic_id: Union[str, NotGiven] = NOT_GIVEN
    ) -> list[Document]:
        """List documents for a knowledge base, optionally filtered by topic."""
        params = filter_not_given({"topic_id": topic_id})
        data = self._client.get(
            f"/knowledge-bases/{knowledge_base_id}/documents",
            params=params,
        )
        return [Document.from_dict(doc) for doc in data]
