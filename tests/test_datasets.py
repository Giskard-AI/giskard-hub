from unittest.mock import MagicMock

import pytest

from giskard_hub.data.dataset import Dataset
from giskard_hub.resources.datasets import DatasetsResource


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
            if cast_to == Dataset:
                return [
                    Dataset.from_dict(item, _client=mock_client)
                    for item in response_data
                ]
        else:
            if cast_to == Dataset:
                return Dataset.from_dict(response_data, _client=mock_client)

        return response_data

    # GET
    mock_client.get.side_effect = handle_get_response

    # POST
    mock_client.post.side_effect = lambda path, cast_to=None, **kwargs: (
        Dataset.from_dict(mock_client.post.return_value, _client=mock_client)
        if cast_to == Dataset
        else mock_client.post.return_value
    )

    # PATCH
    mock_client.patch.side_effect = lambda path, cast_to=None, **kwargs: (
        Dataset.from_dict(mock_client.patch.return_value, _client=mock_client)
        if cast_to == Dataset
        else mock_client.patch.return_value
    )

    # DELETE
    mock_client.delete.side_effect = lambda path, **kwargs: None

    return mock_client


class TestDatasetsResource:
    """Test the DatasetsResource class."""

    def test_retrieve(self, mock_client):
        """Test retrieving a dataset."""
        resource = DatasetsResource(mock_client)

        # Mock the response
        mock_dataset_data = {
            "id": "dataset-1",
            "name": "Test Dataset",
            "description": "A test dataset",
            "project_id": "project-1",
            "tags": ["test", "sample"],
        }
        mock_client.get.return_value = mock_dataset_data

        result = resource.retrieve("dataset-1")

        mock_client.get.assert_called_once_with("/datasets/dataset-1", cast_to=Dataset)
        assert result.id == "dataset-1"
        assert result.name == "Test Dataset"
        assert result.description == "A test dataset"
        assert result.project_id == "project-1"
        assert result.tags == ["test", "sample"]

    def test_create(self, mock_client):
        """Test creating a dataset."""
        resource = DatasetsResource(mock_client)

        # Mock the response
        mock_created_data = {
            "id": "dataset-new",
            "name": "New Dataset",
            "description": "A newly created dataset",
            "project_id": "project-1",
            "tags": [],
        }
        mock_client.post.return_value = mock_created_data

        result = resource.create(
            name="New Dataset",
            description="A newly created dataset",
            project_id="project-1",
        )

        mock_client.post.assert_called_once()
        call_args = mock_client.post.call_args
        assert call_args[0][0] == "/datasets"
        assert call_args[1]["json"]["name"] == "New Dataset"
        assert call_args[1]["json"]["description"] == "A newly created dataset"
        assert call_args[1]["json"]["project_id"] == "project-1"
        assert call_args[1]["cast_to"] == Dataset
        assert result.id == "dataset-new"
        assert result.name == "New Dataset"

    def test_update(self, mock_client):
        """Test updating a dataset."""
        resource = DatasetsResource(mock_client)

        # Mock the response
        mock_updated_data = {
            "id": "dataset-1",
            "name": "Updated Dataset Name",
            "description": "Updated description",
            "project_id": "project-1",
            "tags": [],
        }
        mock_client.patch.return_value = mock_updated_data

        result = resource.update(
            "dataset-1",
            name="Updated Dataset Name",
            description="Updated description",
        )

        mock_client.patch.assert_called_once()
        call_args = mock_client.patch.call_args
        assert call_args[0][0] == "/datasets/dataset-1"
        json_data = call_args[1]["json"]
        assert json_data["name"] == "Updated Dataset Name"
        assert json_data["description"] == "Updated description"
        assert "project_id" not in json_data  # Should be filtered out as NOT_GIVEN
        assert result.name == "Updated Dataset Name"

    def test_update_partial(self, mock_client):
        """Test partial update of a dataset."""
        resource = DatasetsResource(mock_client)

        # Mock the response
        mock_updated_data = {
            "id": "dataset-1",
            "name": "Original Name",
            "description": "Updated description only",
            "project_id": "project-1",
            "tags": [],
        }
        mock_client.patch.return_value = mock_updated_data

        resource.update("dataset-1", description="Updated description only")

        call_args = mock_client.patch.call_args
        json_data = call_args[1]["json"]
        # Only description should be in the payload
        assert json_data == {"description": "Updated description only"}

    def test_delete_single(self, mock_client):
        """Test deleting a single dataset."""
        resource = DatasetsResource(mock_client)

        resource.delete("dataset-1")

        mock_client.delete.assert_called_once_with(
            "/datasets",
            params={"datasets_ids": "dataset-1"},
        )

    def test_delete_multiple(self, mock_client):
        """Test deleting multiple datasets."""
        resource = DatasetsResource(mock_client)

        resource.delete(["dataset-1", "dataset-2", "dataset-3"])

        mock_client.delete.assert_called_once_with(
            "/datasets",
            params={"datasets_ids": ["dataset-1", "dataset-2", "dataset-3"]},
        )

    def test_list(self, mock_client):
        """Test listing datasets."""
        resource = DatasetsResource(mock_client)

        # Mock the response
        mock_datasets_data = [
            {
                "id": "dataset-1",
                "name": "Dataset 1",
                "description": "First dataset",
                "project_id": "project-1",
                "tags": ["test"],
            },
            {
                "id": "dataset-2",
                "name": "Dataset 2",
                "description": "Second dataset",
                "project_id": "project-1",
                "tags": ["production"],
            },
        ]
        mock_client.get.return_value = mock_datasets_data

        result = resource.list(project_id="project-1")

        mock_client.get.assert_called_once_with(
            "/datasets",
            params={"project_id": "project-1"},
            cast_to=Dataset,
        )
        assert len(result) == 2
        assert result[0].id == "dataset-1"
        assert result[0].name == "Dataset 1"
        assert result[1].id == "dataset-2"
        assert result[1].name == "Dataset 2"

    def test_generate_basic(self, mock_client):
        """Test basic dataset generation."""
        resource = DatasetsResource(mock_client)

        # Mock the response
        mock_generated_data = {
            "id": "dataset-generated",
            "name": "Generated Dataset",
            "description": "",
            "project_id": "project-1",
            "tags": [],
        }
        mock_client.post.return_value = mock_generated_data

        result = resource.generate_adversarial(model_id="model-1")

        mock_client.post.assert_called_once()
        call_args = mock_client.post.call_args
        assert call_args[0][0] == "/datasets/generate"
        json_data = call_args[1]["json"]
        assert json_data["model_id"] == "model-1"
        assert json_data["dataset_name"] == "Generated Dataset"
        assert json_data["description"] == ""
        assert json_data["nb_examples"] == 10
        assert "categories" not in json_data  # Should be filtered out as NOT_GIVEN
        assert call_args[1]["cast_to"] == Dataset
        assert result.id == "dataset-generated"

    def test_generate_with_options(self, mock_client):
        """Test dataset generation with all options."""
        resource = DatasetsResource(mock_client)

        # Mock the response
        mock_generated_data = {
            "id": "dataset-custom",
            "name": "Custom Generated Dataset",
            "description": "A custom generated dataset",
            "project_id": "project-1",
            "tags": [],
        }
        mock_client.post.return_value = mock_generated_data

        categories = [
            {"id": "cat1", "name": "Safety", "desc": "Safety-related issues"},
            {"id": "cat2", "name": "Performance", "desc": "Performance issues"},
        ]

        resource.generate_adversarial(
            model_id="model-2",
            dataset_name="Custom Generated Dataset",
            description="A custom generated dataset",
            categories=categories,
            n_examples=20,
        )

        call_args = mock_client.post.call_args
        json_data = call_args[1]["json"]
        assert json_data["model_id"] == "model-2"
        assert json_data["dataset_name"] == "Custom Generated Dataset"
        assert json_data["description"] == "A custom generated dataset"
        assert json_data["categories"] == categories
        assert json_data["nb_examples"] == 20

    def test_generate_document_based_basic(self, mock_client):
        """Test basic knowledge-based dataset generation."""
        resource = DatasetsResource(mock_client)

        # Mock the response
        mock_generated_data = {
            "id": "dataset-knowledge",
            "name": "Generated Dataset",
            "description": "",
            "project_id": "project-1",
            "tags": [],
        }
        mock_client.post.return_value = mock_generated_data

        result = resource.generate_document_based(
            model_id="model-1",
            knowledge_base_id="kb-1",
        )

        mock_client.post.assert_called_once()
        call_args = mock_client.post.call_args
        assert call_args[0][0] == "/datasets/generate/knowledge"
        json_data = call_args[1]["json"]
        assert json_data["model_id"] == "model-1"
        assert json_data["knowledge_base_id"] == "kb-1"
        assert json_data["dataset_name"] == "Generated Dataset"
        assert json_data["description"] == ""
        assert json_data["nb_questions"] == 10
        assert json_data["topic_ids"] == []
        assert call_args[1]["cast_to"] == Dataset
        assert result.id == "dataset-knowledge"

    def test_generate_document_based_with_options(self, mock_client):
        """Test knowledge-based dataset generation with all options."""
        resource = DatasetsResource(mock_client)

        # Mock the response
        mock_generated_data = {
            "id": "dataset-knowledge-custom",
            "name": "Custom Knowledge Dataset",
            "description": "Generated from knowledge base",
            "project_id": "project-1",
            "tags": [],
        }
        mock_client.post.return_value = mock_generated_data

        topic_ids = ["topic-1", "topic-2", "topic-3"]

        resource.generate_document_based(
            model_id="model-3",
            knowledge_base_id="kb-2",
            dataset_name="Custom Knowledge Dataset",
            description="Generated from knowledge base",
            n_questions=25,
            topic_ids=topic_ids,
        )

        call_args = mock_client.post.call_args
        json_data = call_args[1]["json"]
        assert json_data["model_id"] == "model-3"
        assert json_data["knowledge_base_id"] == "kb-2"
        assert json_data["dataset_name"] == "Custom Knowledge Dataset"
        assert json_data["description"] == "Generated from knowledge base"
        assert json_data["nb_questions"] == 25
        assert json_data["topic_ids"] == topic_ids

    def test_generate_document_based_none_topic_ids(self, mock_client):
        """Test knowledge generation with None topic_ids converts to empty list."""
        resource = DatasetsResource(mock_client)

        # Mock the response
        mock_generated_data = {
            "id": "dataset-knowledge-none",
            "name": "Generated Dataset",
            "description": "",
            "project_id": "project-1",
            "tags": [],
        }
        mock_client.post.return_value = mock_generated_data

        resource.generate_document_based(
            model_id="model-1",
            knowledge_base_id="kb-1",
            topic_ids=None,  # Should be converted to empty list
        )

        call_args = mock_client.post.call_args
        json_data = call_args[1]["json"]
        assert json_data["topic_ids"] == []


class TestDatasetDataModel:
    """Test the Dataset data model."""

    def test_dataset_from_dict_basic(self):
        """Test creating Dataset from basic dict."""
        data = {
            "id": "dataset-1",
            "name": "Test Dataset",
            "description": "A test dataset",
            "project_id": "project-1",
            "tags": ["test", "sample"],
        }

        result = Dataset.from_dict(data)

        assert result.id == "dataset-1"
        assert result.name == "Test Dataset"
        assert result.description == "A test dataset"
        assert result.project_id == "project-1"
        assert result.tags == ["test", "sample"]

    def test_dataset_from_dict_minimal(self):
        """Test creating Dataset with minimal required fields."""
        data = {
            "name": "Minimal Dataset",
        }

        result = Dataset.from_dict(data)

        assert result.name == "Minimal Dataset"
        assert result.description is None  # from_dict doesn't populate defaults
        assert result.project_id is None
        assert result.tags is None  # from_dict doesn't populate defaults

    def test_dataset_chat_test_cases_property_with_client(self):
        """Test chat_test_cases property with a client."""
        mock_client = MagicMock()
        mock_client.chat_test_cases.list.return_value = ["test_case_1", "test_case_2"]

        dataset = Dataset.from_dict(
            {
                "id": "dataset-1",
                "name": "Test Dataset",
            },
            _client=mock_client,
        )

        result = dataset.chat_test_cases

        mock_client.chat_test_cases.list.assert_called_once_with(dataset_id="dataset-1")
        assert result == ["test_case_1", "test_case_2"]

    def test_dataset_chat_test_cases_property_without_client(self):
        """Test chat_test_cases property without a client returns None."""
        dataset = Dataset(name="Test Dataset")

        result = dataset.chat_test_cases

        assert result is None

    def test_dataset_chat_test_cases_property_without_id(self):
        """Test chat_test_cases property without an ID returns None."""
        mock_client = MagicMock()
        dataset = Dataset(name="Test Dataset")
        dataset._client = mock_client

        result = dataset.chat_test_cases

        assert result is None

    def test_dataset_create_chat_test_case_with_client(self):
        """Test create_chat_test_case with a client."""
        from giskard_hub.data.chat import ChatMessage
        from giskard_hub.data.chat_test_case import ChatTestCase

        mock_client = MagicMock()
        mock_client.chat_test_cases.create.return_value = "created_test_case"

        dataset = Dataset.from_dict(
            {
                "id": "dataset-1",
                "name": "Test Dataset",
            },
            _client=mock_client,
        )

        chat_test_case = ChatTestCase(
            messages=[ChatMessage(role="user", content="Hello")],
            demo_output=None,
        )

        result = dataset.create_chat_test_case(chat_test_case)

        mock_client.chat_test_cases.create.assert_called_once()
        assert result == "created_test_case"

    def test_dataset_create_chat_test_case_without_client(self):
        """Test create_chat_test_case without client raises error."""
        from giskard_hub.data.chat import ChatMessage
        from giskard_hub.data.chat_test_case import ChatTestCase

        dataset = Dataset(name="Test Dataset")
        chat_test_case = ChatTestCase(
            messages=[ChatMessage(role="user", content="Hello")],
            demo_output=None,
        )

        with pytest.raises(ValueError, match="detached or unsaved"):
            dataset.create_chat_test_case(chat_test_case)
