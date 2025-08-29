from unittest.mock import MagicMock

import pytest

from giskard_hub.data.knowledge_base import Document, KnowledgeBase, Topic
from giskard_hub.resources.knowledge_bases import KnowledgeBasesResource


@pytest.fixture
def mock_client():
    """Mock client for testing."""
    mock_client = MagicMock()

    def handle_get_response(path, cast_to=None, **kwargs):
        response_data = mock_client.get.return_value
        if cast_to is None:
            return response_data

        # Handle lists vs single items
        if isinstance(response_data, list):
            if cast_to == KnowledgeBase:
                return [
                    KnowledgeBase.from_dict(item, _client=mock_client)
                    for item in response_data
                ]
            if cast_to == Topic:
                return [
                    Topic.from_dict(item, _client=mock_client) for item in response_data
                ]
            if cast_to == Document:
                return [
                    Document.from_dict(item, _client=mock_client)
                    for item in response_data
                ]
        else:
            if cast_to == KnowledgeBase:
                return KnowledgeBase.from_dict(response_data, _client=mock_client)
            if cast_to == Topic:
                return Topic.from_dict(response_data, _client=mock_client)
            if cast_to == Document:
                return Document.from_dict(response_data, _client=mock_client)

        return response_data

    # GET
    mock_client.get.side_effect = handle_get_response

    # POST
    mock_client.post.side_effect = lambda path, cast_to=None, **kwargs: (
        KnowledgeBase.from_dict(mock_client.post.return_value, _client=mock_client)
        if cast_to == KnowledgeBase
        else mock_client.post.return_value
    )

    # PATCH
    mock_client.patch.side_effect = lambda path, cast_to=None, **kwargs: (
        KnowledgeBase.from_dict(mock_client.patch.return_value, _client=mock_client)
        if cast_to == KnowledgeBase
        else mock_client.patch.return_value
    )

    # DELETE
    mock_client.delete.side_effect = lambda path, **kwargs: None

    return mock_client


class TestKnowledgeBasesResource:
    """Test the KnowledgeBasesResource class."""

    def test_retrieve(self, mock_client):
        """Test retrieving a knowledge base."""
        resource = KnowledgeBasesResource(mock_client)

        # Mock the response
        mock_kb_data = {
            "id": "test-id",
            "project_id": "project-id",
            "name": "Test KB",
            "description": "Test description",
            "n_documents": 5,
            "status": {"state": "finished", "current": 5, "total": 5},
            "topics": [],
        }
        mock_client.get.return_value = mock_kb_data

        result = resource.retrieve("test-id")

        mock_client.get.assert_called_once_with(
            "/knowledge-bases/test-id", cast_to=KnowledgeBase
        )
        assert result.id == "test-id"
        assert result.name == "Test KB"

    def test_list(self, mock_client):
        """Test listing knowledge bases."""
        resource = KnowledgeBasesResource(mock_client)

        # Mock the response
        mock_kbs_data = [
            {
                "id": "kb1",
                "project_id": "project-id",
                "name": "KB 1",
                "description": "First KB",
                "n_documents": 5,
                "status": {"state": "finished", "current": 5, "total": 5},
                "topics": [],
            },
            {
                "id": "kb2",
                "project_id": "project-id",
                "name": "KB 2",
                "description": "Second KB",
                "n_documents": 10,
                "status": {"state": "finished", "current": 10, "total": 10},
                "topics": [],
            },
        ]
        mock_client.get.return_value = mock_kbs_data

        result = resource.list(project_id="project-id")

        mock_client.get.assert_called_once_with(
            "/knowledge-bases",
            params={"project_id": "project-id"},
            cast_to=KnowledgeBase,
        )
        assert len(result) == 2
        assert result[0].id == "kb1"
        assert result[1].id == "kb2"

    def test_list_topics(self, mock_client):
        """Test listing topics for a knowledge base."""
        resource = KnowledgeBasesResource(mock_client)

        # Mock the response
        mock_topics_data = [
            {"id": "topic1", "name": "Topic 1", "knowledge_base_id": "kb1"},
            {"id": "topic2", "name": "Topic 2", "knowledge_base_id": "kb1"},
        ]
        mock_client.get.return_value = mock_topics_data

        result = resource.list_topics("kb1")

        mock_client.get.assert_called_once_with(
            "/knowledge-bases/kb1/topics", cast_to=Topic
        )
        assert len(result) == 2
        assert result[0].id == "topic1"
        assert result[1].id == "topic2"

    def test_list_documents(self, mock_client):
        """Test listing documents for a knowledge base."""
        resource = KnowledgeBasesResource(mock_client)

        # Mock the response
        mock_docs_data = [
            {
                "id": "doc1",
                "knowledge_base_id": "kb1",
                "content": "Document 1 content",
                "topic_id": "topic1",
                "embedding": [0.1, 0.2, 0.3],
            },
            {
                "id": "doc2",
                "knowledge_base_id": "kb1",
                "content": "Document 2 content",
                "topic_id": "topic2",
                "embedding": [0.4, 0.5, 0.6],
            },
        ]
        mock_client.get.return_value = mock_docs_data

        result = resource.list_documents("kb1")

        mock_client.get.assert_called_once_with(
            "/knowledge-bases/kb1/documents", params={}, cast_to=Document
        )
        assert len(result) == 2
        assert result[0].id == "doc1"
        assert result[1].id == "doc2"

    def test_list_documents_with_topic_filter(self, mock_client):
        """Test listing documents filtered by topic."""
        resource = KnowledgeBasesResource(mock_client)

        # Mock the response
        mock_docs_data = [
            {
                "id": "doc1",
                "knowledge_base_id": "kb1",
                "content": "Document 1 content",
                "topic_id": "topic1",
                "embedding": [0.1, 0.2, 0.3],
            }
        ]
        mock_client.get.return_value = mock_docs_data

        result = resource.list_documents("kb1", topic_id="topic1")

        mock_client.get.assert_called_once_with(
            "/knowledge-bases/kb1/documents",
            params={"topic_id": "topic1"},
            cast_to=Document,
        )
        assert len(result) == 1
        assert result[0].id == "doc1"
