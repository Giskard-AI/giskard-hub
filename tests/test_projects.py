from unittest.mock import Mock

import pytest

from giskard_hub.data.project import FailureCategory, Project
from giskard_hub.errors import (
    HubAPIError,
    HubAuthenticationError,
    HubForbiddenError,
    HubJSONDecodeError,
    HubValidationError,
)
from giskard_hub.resources.projects import ProjectsResource

TEST_FAILURE_CATEGORY_DATA = {
    "identifier": "hallucination",
    "title": "Hallucination",
    "description": "Model generated false or misleading information",
}

TEST_FAILURE_CATEGORY_DATA_2 = {
    "identifier": "bias",
    "title": "Bias",
    "description": "Model response shows unfair bias",
}

TEST_PROJECT_DATA = {
    "id": "proj_123",
    "name": "Test Project",
    "description": "A test project for unit testing",
    "failure_categories": [TEST_FAILURE_CATEGORY_DATA, TEST_FAILURE_CATEGORY_DATA_2],
}

TEST_PROJECT_DATA_MINIMAL = {
    "id": "proj_minimal",
    "name": "Minimal Project",
    "description": "",
    "failure_categories": [],
}

TEST_PROJECT_LIST_DATA = [
    TEST_PROJECT_DATA,
    TEST_PROJECT_DATA_MINIMAL,
    {
        "id": "proj_456",
        "name": "Another Project",
        "description": "Another test project",
        "failure_categories": [],
    },
]


@pytest.fixture
def mock_client():
    """Create a mock client for testing."""
    client = Mock()
    return client


@pytest.fixture
def projects_resource(mock_client):
    """Create a ProjectsResource instance with mock client."""
    resource = ProjectsResource(mock_client)
    return resource


# Tests for ProjectsResource.retrieve()
def test_retrieve_success(projects_resource, mock_client):
    """Test successful retrieval of project."""
    mock_client.get.return_value = TEST_PROJECT_DATA

    result = projects_resource.retrieve("proj_123")

    mock_client.get.assert_called_once_with("/projects/proj_123", cast_to=Project)
    assert result == TEST_PROJECT_DATA


def test_retrieve_not_found(projects_resource, mock_client):
    """Test retrieve with non-existent project ID."""
    mock_client.get.side_effect = HubAPIError("Project not found", status_code=404)

    with pytest.raises(HubAPIError) as exc_info:
        projects_resource.retrieve("nonexistent_proj")

    assert exc_info.value.status_code == 404
    mock_client.get.assert_called_once_with(
        "/projects/nonexistent_proj", cast_to=Project
    )


def test_retrieve_authentication_error(projects_resource, mock_client):
    """Test retrieve with authentication error."""
    mock_client.get.side_effect = HubAuthenticationError(
        "Authentication failed", status_code=401
    )

    with pytest.raises(HubAuthenticationError):
        projects_resource.retrieve("proj_123")


def test_retrieve_forbidden_error(projects_resource, mock_client):
    """Test retrieve with forbidden access."""
    mock_client.get.side_effect = HubForbiddenError("Access denied", status_code=403)

    with pytest.raises(HubForbiddenError):
        projects_resource.retrieve("proj_123")


# Tests for ProjectsResource.create()
def test_create_success_minimal_params(projects_resource, mock_client):
    """Test successful creation with minimal required parameters."""
    mock_client.post.return_value = TEST_PROJECT_DATA_MINIMAL

    result = projects_resource.create(name="Minimal Project")

    expected_data = {"name": "Minimal Project", "description": ""}

    mock_client.post.assert_called_once_with(
        "/projects", json=expected_data, cast_to=Project
    )
    assert result == TEST_PROJECT_DATA_MINIMAL


def test_create_success_with_description(projects_resource, mock_client):
    """Test successful creation with name and description."""
    mock_client.post.return_value = TEST_PROJECT_DATA

    result = projects_resource.create(
        name="Test Project", description="A test project for unit testing"
    )

    expected_data = {
        "name": "Test Project",
        "description": "A test project for unit testing",
    }

    mock_client.post.assert_called_once_with(
        "/projects", json=expected_data, cast_to=Project
    )
    assert result == TEST_PROJECT_DATA


def test_create_validation_error(projects_resource, mock_client):
    """Test create with validation error for invalid parameters."""
    mock_client.post.side_effect = HubValidationError(
        "Validation failed: name is required", status_code=422
    )

    with pytest.raises(HubValidationError) as exc_info:
        projects_resource.create(name="")  # Invalid empty name

    assert exc_info.value.status_code == 422
    assert "name is required" in str(exc_info.value)


def test_create_api_error(projects_resource, mock_client):
    """Test create with general API error."""
    mock_client.post.side_effect = HubAPIError("Internal server error", status_code=500)

    with pytest.raises(HubAPIError) as exc_info:
        projects_resource.create(name="Test Project")

    assert exc_info.value.status_code == 500


# Tests for ProjectsResource.update()
def test_update_success_name_only(projects_resource, mock_client):
    """Test successful update with name only."""
    updated_project = TEST_PROJECT_DATA.copy()
    updated_project["name"] = "Updated Project Name"
    mock_client.patch.return_value = updated_project

    result = projects_resource.update("proj_123", name="Updated Project Name")

    expected_data = {"name": "Updated Project Name"}

    mock_client.patch.assert_called_once_with(
        "/projects/proj_123", json=expected_data, cast_to=Project
    )
    assert result == updated_project


def test_update_success_description_only(projects_resource, mock_client):
    """Test successful update with description only."""
    updated_project = TEST_PROJECT_DATA.copy()
    updated_project["description"] = "Updated description"
    mock_client.patch.return_value = updated_project

    result = projects_resource.update("proj_123", description="Updated description")

    expected_data = {"description": "Updated description"}

    mock_client.patch.assert_called_once_with(
        "/projects/proj_123", json=expected_data, cast_to=Project
    )
    assert result == updated_project


def test_update_success_failure_categories_only(projects_resource, mock_client):
    """Test successful update with failure categories only."""
    failure_categories = [FailureCategory.from_dict(TEST_FAILURE_CATEGORY_DATA)]
    updated_project = TEST_PROJECT_DATA.copy()
    mock_client.patch.return_value = updated_project

    result = projects_resource.update("proj_123", failure_categories=failure_categories)

    # FailureCategory objects get converted to dicts via maybe_to_dict()
    expected_data = {"failure_categories": [TEST_FAILURE_CATEGORY_DATA]}

    mock_client.patch.assert_called_once_with(
        "/projects/proj_123", json=expected_data, cast_to=Project
    )
    assert result == updated_project


def test_update_success_all_params(projects_resource, mock_client):
    """Test successful update with all parameters."""
    failure_categories = [
        FailureCategory.from_dict(TEST_FAILURE_CATEGORY_DATA),
        FailureCategory.from_dict(TEST_FAILURE_CATEGORY_DATA_2),
    ]
    updated_project = TEST_PROJECT_DATA.copy()
    mock_client.patch.return_value = updated_project

    result = projects_resource.update(
        "proj_123",
        name="Updated Project",
        description="Updated description",
        failure_categories=failure_categories,
    )

    # FailureCategory objects get converted to dicts via maybe_to_dict()
    expected_data = {
        "name": "Updated Project",
        "description": "Updated description",
        "failure_categories": [
            TEST_FAILURE_CATEGORY_DATA,
            TEST_FAILURE_CATEGORY_DATA_2,
        ],
    }

    mock_client.patch.assert_called_once_with(
        "/projects/proj_123", json=expected_data, cast_to=Project
    )
    assert result == updated_project


def test_update_success_no_params(projects_resource, mock_client):
    """Test update with no parameters (should send empty data)."""
    mock_client.patch.return_value = TEST_PROJECT_DATA

    result = projects_resource.update("proj_123")

    expected_data = {}

    mock_client.patch.assert_called_once_with(
        "/projects/proj_123", json=expected_data, cast_to=Project
    )
    assert result == TEST_PROJECT_DATA


def test_update_validation_error(projects_resource, mock_client):
    """Test update with validation error."""
    mock_client.patch.side_effect = HubValidationError(
        "Validation failed: invalid project data", status_code=422
    )

    with pytest.raises(HubValidationError) as exc_info:
        projects_resource.update("proj_123", name="")  # Invalid empty name

    assert exc_info.value.status_code == 422


def test_update_not_found(projects_resource, mock_client):
    """Test update with non-existent project ID."""
    mock_client.patch.side_effect = HubAPIError("Project not found", status_code=404)

    with pytest.raises(HubAPIError) as exc_info:
        projects_resource.update("nonexistent_proj", name="Updated Name")

    assert exc_info.value.status_code == 404


def test_update_forbidden(projects_resource, mock_client):
    """Test update with forbidden access."""
    mock_client.patch.side_effect = HubForbiddenError(
        "Cannot update project", status_code=403
    )

    with pytest.raises(HubForbiddenError):
        projects_resource.update("proj_123", name="Updated Name")


# Tests for ProjectsResource.delete()
def test_delete_single_project_id(projects_resource, mock_client):
    """Test deletion with single project ID."""
    mock_client.delete.return_value = {"success": True}

    result = projects_resource.delete("proj_123")

    mock_client.delete.assert_called_once_with(
        "/projects", params={"project_ids": "proj_123"}
    )
    assert result == {"success": True}


def test_delete_multiple_project_ids(projects_resource, mock_client):
    """Test deletion with multiple project IDs."""
    mock_client.delete.return_value = {"success": True}
    project_ids = ["proj_123", "proj_456", "proj_789"]

    result = projects_resource.delete(project_ids)

    mock_client.delete.assert_called_once_with(
        "/projects", params={"project_ids": project_ids}
    )
    assert result == {"success": True}


def test_delete_not_found(projects_resource, mock_client):
    """Test delete with non-existent project ID."""
    mock_client.delete.side_effect = HubAPIError("Project not found", status_code=404)

    with pytest.raises(HubAPIError) as exc_info:
        projects_resource.delete("nonexistent_proj")

    assert exc_info.value.status_code == 404


def test_delete_forbidden(projects_resource, mock_client):
    """Test delete with forbidden access."""
    mock_client.delete.side_effect = HubForbiddenError(
        "Cannot delete project", status_code=403
    )

    with pytest.raises(HubForbiddenError):
        projects_resource.delete("proj_123")


def test_delete_validation_error(projects_resource, mock_client):
    """Test delete with validation error (e.g., project has dependencies)."""
    mock_client.delete.side_effect = HubValidationError(
        "Cannot delete project: has active evaluations", status_code=422
    )

    with pytest.raises(HubValidationError) as exc_info:
        projects_resource.delete("proj_123")

    assert exc_info.value.status_code == 422
    assert "has active evaluations" in str(exc_info.value)


# Tests for ProjectsResource.list()
def test_list_success(projects_resource, mock_client):
    """Test successful listing of projects."""
    mock_client.get.return_value = TEST_PROJECT_LIST_DATA

    result = projects_resource.list()

    mock_client.get.assert_called_once_with("/projects")
    assert len(result) == 3
    assert all(isinstance(project, Project) for project in result)


def test_list_empty(projects_resource, mock_client):
    """Test listing projects when no projects exist."""
    mock_client.get.return_value = []

    result = projects_resource.list()

    mock_client.get.assert_called_once_with("/projects")
    assert result == []


def test_list_authentication_error(projects_resource, mock_client):
    """Test list with authentication error."""
    mock_client.get.side_effect = HubAuthenticationError(
        "Authentication failed", status_code=401
    )

    with pytest.raises(HubAuthenticationError):
        projects_resource.list()


def test_list_forbidden_error(projects_resource, mock_client):
    """Test list with forbidden access."""
    mock_client.get.side_effect = HubForbiddenError("Access denied", status_code=403)

    with pytest.raises(HubForbiddenError):
        projects_resource.list()


def test_list_api_error(projects_resource, mock_client):
    """Test list with general API error."""
    mock_client.get.side_effect = HubAPIError("Internal server error", status_code=500)

    with pytest.raises(HubAPIError) as exc_info:
        projects_resource.list()

    assert exc_info.value.status_code == 500


def test_list_json_decode_error(projects_resource, mock_client):
    """Test list with JSON decode error."""
    mock_client.get.side_effect = HubJSONDecodeError(
        "Invalid JSON response", status_code=200
    )

    with pytest.raises(HubJSONDecodeError):
        projects_resource.list()


# Tests for edge cases and data validation
def test_update_with_empty_failure_categories(projects_resource, mock_client):
    """Test update with empty failure categories list."""
    updated_project = TEST_PROJECT_DATA_MINIMAL.copy()
    mock_client.patch.return_value = updated_project

    result = projects_resource.update("proj_123", failure_categories=[])

    expected_data = {"failure_categories": []}

    mock_client.patch.assert_called_once_with(
        "/projects/proj_123", json=expected_data, cast_to=Project
    )
    assert result == updated_project


def test_update_with_none_failure_categories(projects_resource, mock_client):
    """Test update with None failure categories."""
    updated_project = TEST_PROJECT_DATA.copy()
    mock_client.patch.return_value = updated_project

    result = projects_resource.update("proj_123", failure_categories=None)

    expected_data = {"failure_categories": None}

    mock_client.patch.assert_called_once_with(
        "/projects/proj_123", json=expected_data, cast_to=Project
    )
    assert result == updated_project


def test_create_with_empty_description(projects_resource, mock_client):
    """Test create with explicitly empty description."""
    mock_client.post.return_value = TEST_PROJECT_DATA_MINIMAL

    result = projects_resource.create(name="Test Project", description="")

    expected_data = {"name": "Test Project", "description": ""}

    mock_client.post.assert_called_once_with(
        "/projects", json=expected_data, cast_to=Project
    )
    assert result == TEST_PROJECT_DATA_MINIMAL


def test_list_with_failure_categories(projects_resource, mock_client):
    """Test listing projects that include failure categories."""
    # Use project data without failure categories to avoid conversion issues
    project_data_without_categories = {
        "id": "proj_123",
        "name": "Test Project",
        "description": "A test project for unit testing",
        "failure_categories": [],
    }
    mock_client.get.return_value = [project_data_without_categories]

    result = projects_resource.list()

    mock_client.get.assert_called_once_with("/projects")
    assert len(result) == 1
    project = result[0]
    assert isinstance(project, Project)
    assert project.name == "Test Project"
    assert project.description == "A test project for unit testing"
    assert len(project.failure_categories) == 0
