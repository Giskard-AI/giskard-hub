from unittest.mock import MagicMock

import pytest

from giskard_hub.data.check import Check
from giskard_hub.errors import (
    HubAPIError,
    HubValidationError,
)
from giskard_hub.resources.checks import ChecksResource


@pytest.fixture
def mock_client():
    mock_client = MagicMock()

    # GET
    mock_client.get.side_effect = lambda path, **kwargs: mock_client.get.return_value

    # POST
    mock_client.post.side_effect = (
        lambda path, json=None, **kwargs: mock_client.post.return_value
    )

    # PATCH
    mock_client.patch.side_effect = (
        lambda path, json=None, **kwargs: mock_client.patch.return_value
    )

    # DELETE
    mock_client.delete.side_effect = lambda path, **kwargs: None

    return mock_client


@pytest.fixture
def mock_client_with_errors():
    mock_client = MagicMock()
    return mock_client


@pytest.fixture
def sample_check_data():
    return {
        "id": "check_123",
        "created_at": "2025-06-17T12:46:52.424Z",
        "updated_at": "2025-06-17T12:46:52.424Z",
        "identifier": "custom_correctness",
        "name": "Custom Correctness Check",
        "description": "This is a custom correctness check",
        "assertions": [
            {
                "type": "correctness",
                "reference": "This is a test reference",
            }
        ],
    }


@pytest.fixture
def sample_checks_list_data():
    return [
        {
            "id": "check_123",
            "created_at": "2025-06-17T12:46:52.424Z",
            "updated_at": "2025-06-17T12:46:52.424Z",
            "identifier": "custom_correctness",
            "name": "Custom Correctness Check",
            "description": "This is a custom correctness check",
            "assertions": [
                {
                    "type": "correctness",
                    "reference": "This is a test reference",
                }
            ],
        },
        {
            "id": "check_456",
            "created_at": "2025-06-17T12:46:52.424Z",
            "updated_at": "2025-06-17T12:46:52.424Z",
            "identifier": "custom_conformity",
            "name": "Custom Conformity Check",
            "description": "This is a custom conformity check",
            "assertions": [
                {
                    "type": "conformity",
                    "rules": ["should mention this is a test"],
                }
            ],
        },
    ]


def test_checks_list(mock_client, sample_checks_list_data):
    mock_client.get.return_value = sample_checks_list_data

    checks_resource = ChecksResource(mock_client)
    result = checks_resource.list(project_id="project_123")

    assert mock_client.get.called
    mock_client.get.assert_called_once_with(
        "/checks", params={"project_id": "project_123", "filter_builtin": True}
    )

    assert isinstance(result, list)
    assert len(result) == 2

    # Check first check
    first_check = result[0]
    assert isinstance(first_check, Check)
    assert first_check.id == "check_123"
    assert first_check.identifier == "custom_correctness"
    assert first_check.name == "Custom Correctness Check"
    assert first_check.description == "This is a custom correctness check"
    assert first_check.params == {
        "type": "correctness",
        "reference": "This is a test reference",
    }

    # Check second check
    second_check = result[1]
    assert isinstance(second_check, Check)
    assert second_check.id == "check_456"
    assert second_check.identifier == "custom_conformity"
    assert second_check.name == "Custom Conformity Check"
    assert second_check.description == "This is a custom conformity check"
    assert second_check.params == {
        "type": "conformity",
        "rules": ["should mention this is a test"],
    }


def test_checks_retrieve(mock_client, sample_check_data):
    mock_client.get.return_value = sample_check_data

    checks_resource = ChecksResource(mock_client)
    result = checks_resource.retrieve(check_id="check_123")

    assert mock_client.get.called
    mock_client.get.assert_called_once_with("/checks/check_123")

    assert isinstance(result, Check)
    assert result.id == "check_123"
    assert result.identifier == "custom_correctness"
    assert result.name == "Custom Correctness Check"
    assert result.description == "This is a custom correctness check"
    assert result.params == {
        "type": "correctness",
        "reference": "This is a test reference",
    }


def test_checks_create(mock_client, sample_check_data):
    mock_client.post.return_value = sample_check_data

    checks_resource = ChecksResource(mock_client)
    result = checks_resource.create(
        project_id="project_123",
        identifier="custom_correctness",
        name="Custom Correctness Check",
        description="This is a custom correctness check",
        params={
            "reference": "This is a test reference",
            "type": "correctness",
        },
    )

    assert mock_client.post.called
    mock_client.post.assert_called_once_with(
        "/checks",
        json={
            "project_id": "project_123",
            "description": "This is a custom correctness check",
            "name": "Custom Correctness Check",
            "identifier": "custom_correctness",
            "assertions": [
                {
                    "reference": "This is a test reference",
                    "type": "correctness",
                }
            ],
        },
    )

    assert isinstance(result, Check)
    assert result.id == "check_123"
    assert result.identifier == "custom_correctness"
    assert result.name == "Custom Correctness Check"
    assert result.description == "This is a custom correctness check"
    assert result.params == {
        "type": "correctness",
        "reference": "This is a test reference",
    }


def test_checks_create_without_description(mock_client, sample_check_data):
    mock_client.post.return_value = {
        **sample_check_data,
        "description": None,
    }

    checks_resource = ChecksResource(mock_client)
    result = checks_resource.create(
        project_id="project_123",
        identifier="custom_correctness",
        name="Custom Correctness Check",
        params={
            "reference": "This is a test reference",
            "type": "correctness",
        },
    )

    assert mock_client.post.called
    mock_client.post.assert_called_once_with(
        "/checks",
        json={
            "project_id": "project_123",
            "description": None,
            "name": "Custom Correctness Check",
            "identifier": "custom_correctness",
            "assertions": [
                {
                    "reference": "This is a test reference",
                    "type": "correctness",
                }
            ],
        },
    )

    assert isinstance(result, Check)
    assert result.id == "check_123"
    assert result.description is None


def test_checks_update(mock_client, sample_check_data):
    mock_client.patch.return_value = {
        **sample_check_data,
        "identifier": "updated_correctness",
        "name": "Updated Correctness Check",
        "description": "Updated description",
        "assertions": [
            {
                "reference": "Updated expected response",
                "type": "correctness",
            }
        ],
    }

    checks_resource = ChecksResource(mock_client)
    result = checks_resource.update(
        check_id="check_123",
        identifier="updated_correctness",
        name="Updated Correctness Check",
        description="Updated description",
        params={
            "reference": "Updated expected response",
            "type": "correctness",
        },
    )

    assert mock_client.patch.called
    mock_client.patch.assert_called_once_with(
        "/checks/check_123",
        json={
            "identifier": "updated_correctness",
            "name": "Updated Correctness Check",
            "description": "Updated description",
            "assertions": [
                {
                    "reference": "Updated expected response",
                    "type": "correctness",
                }
            ],
        },
    )

    assert isinstance(result, Check)
    assert result.id == "check_123"
    assert result.identifier == "updated_correctness"
    assert result.name == "Updated Correctness Check"
    assert result.description == "Updated description"
    assert result.params == {
        "type": "correctness",
        "reference": "Updated expected response",
    }


def test_checks_update_partial(mock_client, sample_check_data):
    mock_client.patch.return_value = {
        **sample_check_data,
        "name": "Updated Name Only",
    }

    checks_resource = ChecksResource(mock_client)
    result = checks_resource.update(
        check_id="check_123",
        name="Updated Name Only",
    )

    assert mock_client.patch.called
    mock_client.patch.assert_called_once_with(
        "/checks/check_123",
        json={
            "name": "Updated Name Only",
        },
    )

    assert isinstance(result, Check)
    assert result.id == "check_123"
    assert result.name == "Updated Name Only"


def test_checks_delete_single(mock_client):
    checks_resource = ChecksResource(mock_client)
    result = checks_resource.delete(check_id="check_123")

    assert mock_client.delete.called
    mock_client.delete.assert_called_once_with(
        "/checks", params={"check_ids": "check_123"}
    )

    assert result is None


def test_checks_delete_multiple(mock_client):
    check_ids = ["check_123", "check_456", "check_789"]

    checks_resource = ChecksResource(mock_client)
    result = checks_resource.delete(check_id=check_ids)

    assert mock_client.delete.called
    mock_client.delete.assert_called_once_with(
        "/checks", params={"check_ids": check_ids}
    )

    assert result is None


def test_checks_list_empty_project(mock_client):
    mock_client.get.return_value = []

    checks_resource = ChecksResource(mock_client)
    result = checks_resource.list(project_id="empty_project")

    assert mock_client.get.called
    mock_client.get.assert_called_once_with(
        "/checks", params={"project_id": "empty_project", "filter_builtin": True}
    )

    assert isinstance(result, list)
    assert len(result) == 0


def test_checks_retrieve_not_found_error(mock_client_with_errors):
    mock_client_with_errors.get.side_effect = HubAPIError(
        "Check not found",
        status_code=404,
        response_text="Not Found",
    )

    checks_resource = ChecksResource(mock_client_with_errors)

    with pytest.raises(HubAPIError) as exc_info:
        checks_resource.retrieve(check_id="nonexistent_check")

    assert exc_info.value.status_code == 404
    assert "Check not found" in exc_info.value.message


def test_checks_create_duplicate_identifier_error(mock_client_with_errors):
    mock_client_with_errors.post.side_effect = HubValidationError(
        "Validation error: Check with identifier 'custom_correctness' already exists in this project",
        status_code=422,
        response_text="Unprocessable Entity",
    )

    checks_resource = ChecksResource(mock_client_with_errors)

    with pytest.raises(HubValidationError) as exc_info:
        checks_resource.create(
            project_id="project_123",
            identifier="custom_correctness",
            name="Duplicate Check",
            params={"reference": "This is a test reference", "type": "correctness"},
        )

    assert exc_info.value.status_code == 422
    assert "already exists" in exc_info.value.message


def test_checks_create_missing_required_fields_error(mock_client_with_errors):
    mock_client_with_errors.post.side_effect = HubValidationError(
        "Validation error: Missing required fields\nname: This field is required\nidentifier: This field is required",
        status_code=422,
        response_text="Unprocessable Entity",
    )

    checks_resource = ChecksResource(mock_client_with_errors)

    with pytest.raises(HubValidationError) as exc_info:
        checks_resource.create(
            project_id="project_123",
            identifier="",
            name="",
            params={"reference": "This is a test reference", "type": "correctness"},
        )

    assert exc_info.value.status_code == 422
    assert "Missing required fields" in exc_info.value.message
    assert "name: This field is required" in exc_info.value.message
    assert "identifier: This field is required" in exc_info.value.message
