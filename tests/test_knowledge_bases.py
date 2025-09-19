import tempfile
from pathlib import Path
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
        )
        assert len(result) == 2
        assert result[0].id == "kb1"
        assert result[1].id == "kb2"

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
            "/knowledge-bases/kb1/documents",
            params={},
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
        )
        assert len(result) == 1
        assert result[0].id == "doc1"

    def test_create_with_jsonl_file(self, mock_client):
        """Test creating a knowledge base with a JSONL file (should succeed)."""
        resource = KnowledgeBasesResource(mock_client)

        # Create a temporary JSONL file
        jsonl_content = """{"text": "First document content"}
{"text": "Second document content"}
{"text": "Third document content", "topic": "test-topic"}"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".jsonl", delete=False
        ) as temp_file:
            temp_file.write(jsonl_content)
            temp_file_path = temp_file.name

        try:
            # Mock the response
            mock_kb_data = {
                "id": "kb-jsonl",
                "project_id": "project-id",
                "name": "JSONL Knowledge Base",
                "description": "KB from JSONL file",
                "n_documents": 3,
                "status": {"state": "finished", "current": 3, "total": 3},
                "topics": [],
            }
            mock_client.post.return_value = mock_kb_data

            result = resource.create(
                project_id="project-id",
                name="JSONL Knowledge Base",
                data=temp_file_path,
                description="KB from JSONL file",
            )

            # Verify the API call was made
            mock_client.post.assert_called_once()
            call_args = mock_client.post.call_args
            assert call_args[0][0] == "/knowledge-bases"
            assert call_args[1]["params"]["project_id"] == "project-id"
            assert call_args[1]["params"]["name"] == "JSONL Knowledge Base"
            assert "files" in call_args[1]
            assert result.id == "kb-jsonl"
            assert result.n_documents == 3

        finally:
            # Clean up temp file
            Path(temp_file_path).unlink(missing_ok=True)

    def test_create_with_json_file(self, mock_client):
        """Test creating a knowledge base with a JSON file (should succeed)."""
        resource = KnowledgeBasesResource(mock_client)

        # Create a temporary JSON file
        json_content = """[
    {"text": "First document content"},
    {"text": "Second document content"},
    {"text": "Third document content", "topic": "test-topic"}
]"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as temp_file:
            temp_file.write(json_content)
            temp_file_path = temp_file.name

        try:
            # Mock the response
            mock_kb_data = {
                "id": "kb-json",
                "project_id": "project-id",
                "name": "JSON Knowledge Base",
                "description": "KB from JSON file",
                "n_documents": 3,
                "status": {"state": "finished", "current": 3, "total": 3},
                "topics": [],
            }
            mock_client.post.return_value = mock_kb_data

            result = resource.create(
                project_id="project-id",
                name="JSON Knowledge Base",
                data=temp_file_path,
                description="KB from JSON file",
            )

            # Verify the API call was made
            mock_client.post.assert_called_once()
            call_args = mock_client.post.call_args
            assert call_args[0][0] == "/knowledge-bases"
            assert call_args[1]["params"]["project_id"] == "project-id"
            assert call_args[1]["params"]["name"] == "JSON Knowledge Base"
            assert "files" in call_args[1]
            assert result.id == "kb-json"
            assert result.n_documents == 3

        finally:
            # Clean up temp file
            Path(temp_file_path).unlink(missing_ok=True)

    def test_create_with_list_of_dicts(self, mock_client):
        """Test creating a knowledge base with a list of dictionaries (should succeed)."""
        resource = KnowledgeBasesResource(mock_client)

        # Mock the response
        mock_kb_data = {
            "id": "kb-list",
            "project_id": "project-id",
            "name": "List Knowledge Base",
            "description": "KB from list of dicts",
            "n_documents": 3,
            "status": {"state": "finished", "current": 3, "total": 3},
            "topics": [],
        }
        mock_client.post.return_value = mock_kb_data

        # Test data as list of dictionaries
        test_data = [
            {"text": "First document content"},
            {"text": "Second document content"},
            {"text": "Third document content", "topic": "test-topic"},
        ]

        result = resource.create(
            project_id="project-id",
            name="List Knowledge Base",
            data=test_data,
            description="KB from list of dicts",
        )

        # Verify the API call was made
        mock_client.post.assert_called_once()
        call_args = mock_client.post.call_args
        assert call_args[0][0] == "/knowledge-bases"
        assert call_args[1]["params"]["project_id"] == "project-id"
        assert call_args[1]["params"]["name"] == "List Knowledge Base"
        assert "files" in call_args[1]
        assert result.id == "kb-list"
        assert result.n_documents == 3

    def test_create_with_csv_file_error(self, mock_client):
        """Test creating a knowledge base with a CSV file (should error - not supported)."""
        resource = KnowledgeBasesResource(mock_client)

        # Create a temporary CSV file
        csv_content = """text,topic
First document content,topic1
Second document content,topic2
Third document content,topic3"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False
        ) as temp_file:
            temp_file.write(csv_content)
            temp_file_path = temp_file.name

        try:
            # Test that it raises an error for unsupported file format
            with pytest.raises(
                ValueError,
                match="Only JSON and JSONL files are supported for file input",
            ):
                resource.create(
                    project_id="project-id",
                    name="CSV Knowledge Base",
                    data=temp_file_path,
                )

            # Verify no API call was made due to validation error
            mock_client.post.assert_not_called()

        finally:
            # Clean up temp file
            Path(temp_file_path).unlink(missing_ok=True)

    def test_create_with_single_dict_error(self, mock_client):
        """Test creating a knowledge base with a single dict (should error - needs list)."""
        resource = KnowledgeBasesResource(mock_client)

        # Test data as single dictionary instead of list
        test_data = {"text": "Single document content"}

        # Test that it raises an error because data must be a list of dicts
        with pytest.raises(
            ValueError,
            match="data must be a filepath \\(str\\) or a list of Python dicts",
        ):
            resource.create(
                project_id="project-id",
                name="Single Dict Knowledge Base",
                data=test_data,
            )

        # Verify no API call was made due to validation error
        mock_client.post.assert_not_called()

    def test_create_with_wrong_keys_error(self, mock_client):
        """Test creating a knowledge base with list of dicts with wrong keys (should error)."""
        resource = KnowledgeBasesResource(mock_client)

        # Mock a server-side validation error response
        mock_client.post.side_effect = ValueError(
            "Invalid data format: missing 'text' key"
        )

        # Test data with wrong keys (missing 'text' key)
        test_data = [
            {"content": "First document content"},  # Wrong key: should be 'text'
            {"document": "Second document content"},  # Wrong key: should be 'text'
            {"message": "Third document content"},  # Wrong key: should be 'text'
        ]

        # Test that it raises an error due to wrong keys
        with pytest.raises(ValueError, match="Invalid data format: missing 'text' key"):
            resource.create(
                project_id="project-id",
                name="Wrong Keys Knowledge Base",
                data=test_data,
            )

        # Verify the API call was attempted (validation happens server-side)
        mock_client.post.assert_called_once()
