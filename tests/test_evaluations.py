from unittest.mock import Mock

import pytest

from giskard_hub.data.chat_test_case import ChatTestCase
from giskard_hub.data.evaluation import EvaluationEntry, EvaluationRun, EvaluatorResult
from giskard_hub.data.model import Model, ModelOutput
from giskard_hub.data.task import TaskStatus
from giskard_hub.errors import (
    HubAPIError,
    HubAuthenticationError,
    HubForbiddenError,
    HubJSONDecodeError,
    HubValidationError,
)
from giskard_hub.resources.evaluations import EvaluationsResource

TEST_CONVERSATION_DATA = {
    "id": "conv_123",
    "dataset_id": "ds_456",
    "messages": [
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi there! How can I help you?"},
    ],
    "demo_output": {
        "role": "assistant",
        "content": "This is a demo output.",
        "metadata": {"key": "value"},
    },
    "tags": ["greeting", "test"],
    "checks": [],
}

TEST_MODEL_DATA = {
    "id": "model_123",
    "name": "Test Model",
    "project_id": "proj_456",
    "url": "https://api.example.com/model",
    "description": "A test model",
    "supported_languages": ["en", "fr"],
    "headers": {"Authorization": "Bearer token123"},
}

TEST_EVALUATION_RUN_DATA = {
    "id": "run_123",
    "name": "Test Evaluation Run",
    "project_id": "proj_456",
    "datasets": [],
    "model": TEST_MODEL_DATA,
    "criteria": [{"dataset_id": "ds_456", "tags": ["test"]}],
    "metrics": [],
    "tags": [],
    "failure_categories": {},
    "status": {"status": "COMPLETED", "progress": 100},
}

TEST_EVALUATION_ENTRY_DATA = {
    "id": "entry_123",
    "run_id": "run_123",
    "chat_test_case": TEST_CONVERSATION_DATA,
    "results": [],
    "status": "COMPLETED",
    "model_output": {
        "response": {"role": "assistant", "content": "Test response"},
        "metadata": {"test": "value"},
    },
}

TEST_MODEL_OUTPUT_DATA = {
    "response": {"role": "assistant", "content": "Updated response"},
    "metadata": {"updated": True},
}

TEST_EVALUATOR_RESULTS = [
    {
        "name": "correctness",
        "status": "COMPLETED",
        "passed": True,
        "reason": "Response is correct",
    },
    {
        "name": "relevance",
        "status": "COMPLETED",
        "passed": False,
        "reason": "Response is not relevant",
    },
]

TEST_FAILURE_CATEGORY_DATA = {
    "identifier": "hallucination",
    "title": "Hallucination",
    "description": "Model generated false or misleading information",
}

TEST_FAILURE_CATEGORY_RESULT_DATA = {
    "category": TEST_FAILURE_CATEGORY_DATA,
    "status": "finished",
    "error": None,
}

TEST_EVALUATION_ENTRY_WITH_FAILURE_CATEGORY = {
    "id": "entry_with_failure",
    "run_id": "run_123",
    "chat_test_case": TEST_CONVERSATION_DATA,
    "results": [],
    "status": "FAILED",
    "model_output": {
        "response": {"role": "assistant", "content": "Test response with failure"},
        "metadata": {"test": "value"},
    },
    "failure_category": TEST_FAILURE_CATEGORY_RESULT_DATA,
}


@pytest.fixture
def mock_client():
    """Create a mock client for testing."""
    client = Mock()
    return client


@pytest.fixture
def evaluations_resource(mock_client):
    """Create an EvaluationsResource instance with mock client."""
    resource = EvaluationsResource(mock_client)
    return resource


def test_evaluation_entry_from_chat_test_case():
    chat_test_case_data = TEST_CONVERSATION_DATA.copy()

    chat_test_case = ChatTestCase.from_dict(chat_test_case_data)
    evaluation_entry = EvaluationEntry.from_dict(
        {
            "chat_test_case": chat_test_case_data,
            "run_id": "run_123",
            "results": [],
            "status": TaskStatus.RUNNING,
            "model_output": None,
        }
    )

    assert isinstance(evaluation_entry.chat_test_case, ChatTestCase)
    assert evaluation_entry.chat_test_case.id == chat_test_case.id


# Tests for EvaluationsResource.retrieve()
def test_retrieve_success(evaluations_resource, mock_client):
    """Test successful retrieval of evaluation run."""
    mock_client.get.return_value = TEST_EVALUATION_RUN_DATA

    result = evaluations_resource.retrieve("run_123")

    mock_client.get.assert_called_once_with(
        "/evaluations/run_123", cast_to=EvaluationRun
    )
    assert result == TEST_EVALUATION_RUN_DATA


def test_retrieve_not_found(evaluations_resource, mock_client):
    """Test retrieve with non-existent run ID."""
    mock_client.get.side_effect = HubAPIError(
        "Evaluation run not found", status_code=404
    )

    with pytest.raises(HubAPIError) as exc_info:
        evaluations_resource.retrieve("nonexistent_run")

    assert exc_info.value.status_code == 404
    mock_client.get.assert_called_once_with(
        "/evaluations/nonexistent_run", cast_to=EvaluationRun
    )


def test_retrieve_authentication_error(evaluations_resource, mock_client):
    """Test retrieve with authentication error."""
    mock_client.get.side_effect = HubAuthenticationError(
        "Authentication failed", status_code=401
    )

    with pytest.raises(HubAuthenticationError):
        evaluations_resource.retrieve("run_123")


def test_retrieve_forbidden_error(evaluations_resource, mock_client):
    """Test retrieve with forbidden access."""
    mock_client.get.side_effect = HubForbiddenError("Access denied", status_code=403)

    with pytest.raises(HubForbiddenError):
        evaluations_resource.retrieve("run_123")


# Tests for EvaluationsResource.create()
def test_create_success_minimal_params(evaluations_resource, mock_client):
    """Test successful creation with minimal required parameters."""
    mock_client.post.return_value = TEST_EVALUATION_RUN_DATA

    result = evaluations_resource.create(model_id="model_123", dataset_id="ds_456")

    expected_data = {
        "model_id": "model_123",
        "run_count": 1,
        "criteria": [{"dataset_id": "ds_456"}],
    }

    mock_client.post.assert_called_once_with(
        "/evaluations", json=expected_data, cast_to=EvaluationRun
    )
    assert result == TEST_EVALUATION_RUN_DATA


def test_create_success_all_params(evaluations_resource, mock_client):
    """Test successful creation with all parameters."""
    mock_client.post.return_value = TEST_EVALUATION_RUN_DATA

    result = evaluations_resource.create(
        model_id="model_123",
        dataset_id="ds_456",
        tags=["test", "production"],
        name="My Test Evaluation",
        run_count=5,
    )

    expected_data = {
        "name": "My Test Evaluation",
        "model_id": "model_123",
        "run_count": 5,
        "criteria": [{"dataset_id": "ds_456", "tags": ["test", "production"]}],
    }

    mock_client.post.assert_called_once_with(
        "/evaluations", json=expected_data, cast_to=EvaluationRun
    )
    assert result == TEST_EVALUATION_RUN_DATA


def test_create_validation_error(evaluations_resource, mock_client):
    """Test create with validation error for invalid parameters."""
    mock_client.post.side_effect = HubValidationError(
        "Validation failed: model_id is required", status_code=422
    )

    with pytest.raises(HubValidationError) as exc_info:
        evaluations_resource.create(
            model_id="", dataset_id="ds_456"  # Invalid empty model_id
        )

    assert exc_info.value.status_code == 422
    assert "model_id is required" in str(exc_info.value)


def test_create_api_error(evaluations_resource, mock_client):
    """Test create with general API error."""
    mock_client.post.side_effect = HubAPIError("Internal server error", status_code=500)

    with pytest.raises(HubAPIError) as exc_info:
        evaluations_resource.create(model_id="model_123", dataset_id="ds_456")

    assert exc_info.value.status_code == 500


# Tests for EvaluationsResource.create_local()
def test_create_local_success_minimal_params(evaluations_resource, mock_client):
    """Test successful local creation with minimal required parameters."""
    mock_client.post.return_value = TEST_EVALUATION_RUN_DATA
    model = Model.from_dict(TEST_MODEL_DATA)

    result = evaluations_resource.create_local(model=model, dataset_id="ds_456")

    expected_data = {"model": model.to_dict(), "criteria": [{"dataset_id": "ds_456"}]}

    mock_client.post.assert_called_once_with(
        "/evaluations/local", json=expected_data, cast_to=EvaluationRun
    )
    assert result == TEST_EVALUATION_RUN_DATA


def test_create_local_success_all_params(evaluations_resource, mock_client):
    """Test successful local creation with all parameters."""
    mock_client.post.return_value = TEST_EVALUATION_RUN_DATA
    model = Model.from_dict(TEST_MODEL_DATA)

    result = evaluations_resource.create_local(
        model=model,
        dataset_id="ds_456",
        tags=["local", "test"],
        name="Local Test Evaluation",
    )

    expected_data = {
        "name": "Local Test Evaluation",
        "model": model.to_dict(),
        "criteria": [{"dataset_id": "ds_456", "tags": ["local", "test"]}],
    }

    mock_client.post.assert_called_once_with(
        "/evaluations/local", json=expected_data, cast_to=EvaluationRun
    )
    assert result == TEST_EVALUATION_RUN_DATA


def test_create_local_validation_error(evaluations_resource, mock_client):
    """Test create_local with validation error."""
    mock_client.post.side_effect = HubValidationError(
        "Validation failed: invalid model configuration", status_code=422
    )
    model = Model.from_dict(TEST_MODEL_DATA)

    with pytest.raises(HubValidationError) as exc_info:
        evaluations_resource.create_local(model=model, dataset_id="invalid_dataset")

    assert exc_info.value.status_code == 422


# Tests for EvaluationsResource.delete()
def test_delete_single_evaluation_id(evaluations_resource, mock_client):
    """Test deletion with single evaluation ID."""
    mock_client.delete.return_value = {"success": True}

    result = evaluations_resource.delete("exec_123")

    mock_client.delete.assert_called_once_with(
        "/evaluations", params={"evaluation_ids": "exec_123"}
    )
    assert result == {"success": True}


def test_delete_multiple_evaluation_ids(evaluations_resource, mock_client):
    """Test deletion with multiple evaluation IDs."""
    mock_client.delete.return_value = {"success": True}
    evaluation_ids = ["exec_123", "exec_456", "exec_789"]

    result = evaluations_resource.delete(evaluation_ids)

    mock_client.delete.assert_called_once_with(
        "/evaluations", params={"evaluation_ids": evaluation_ids}
    )
    assert result == {"success": True}


def test_delete_not_found(evaluations_resource, mock_client):
    """Test delete with non-existent evaluation ID."""
    mock_client.delete.side_effect = HubAPIError(
        "Evaluation not found", status_code=404
    )

    with pytest.raises(HubAPIError) as exc_info:
        evaluations_resource.delete("nonexistent_exec")

    assert exc_info.value.status_code == 404


def test_delete_forbidden(evaluations_resource, mock_client):
    """Test delete with forbidden access."""
    mock_client.delete.side_effect = HubForbiddenError(
        "Cannot delete evaluation", status_code=403
    )

    with pytest.raises(HubForbiddenError):
        evaluations_resource.delete("exec_123")


# Tests for EvaluationsResource.list()
def test_list_success(evaluations_resource, mock_client):
    """Test successful listing of evaluations."""
    expected_evaluations = [TEST_EVALUATION_RUN_DATA]
    mock_client.get.return_value = expected_evaluations

    result = evaluations_resource.list("proj_456")

    mock_client.get.assert_called_once_with(
        "/evaluations", params={"project_id": "proj_456"}, cast_to=EvaluationRun
    )
    assert result == expected_evaluations


def test_list_empty_project(evaluations_resource, mock_client):
    """Test listing evaluations for project with no evaluations."""
    mock_client.get.return_value = []

    result = evaluations_resource.list("empty_proj")

    mock_client.get.assert_called_once_with(
        "/evaluations", params={"project_id": "empty_proj"}, cast_to=EvaluationRun
    )
    assert result == []


def test_list_project_not_found(evaluations_resource, mock_client):
    """Test list with non-existent project ID."""
    mock_client.get.side_effect = HubAPIError("Project not found", status_code=404)

    with pytest.raises(HubAPIError) as exc_info:
        evaluations_resource.list("nonexistent_proj")

    assert exc_info.value.status_code == 404


# Tests for EvaluationsResource.list_entries()
def test_list_entries_success(evaluations_resource, mock_client):
    """Test successful listing of evaluation entries."""
    mock_response = {
        "items": [TEST_EVALUATION_ENTRY_DATA, TEST_EVALUATION_ENTRY_DATA.copy()]
    }
    mock_client.get.return_value = mock_response

    result = evaluations_resource.list_entries("run_123")

    mock_client.get.assert_called_once_with(
        "/evaluations/run_123/results?limit=100_000"
    )
    assert len(result) == 2
    assert all(isinstance(entry, EvaluationEntry) for entry in result)


def test_list_entries_empty_run(evaluations_resource, mock_client):
    """Test listing entries for run with no entries."""
    mock_response = {"items": []}
    mock_client.get.return_value = mock_response

    result = evaluations_resource.list_entries("empty_run")

    mock_client.get.assert_called_once_with(
        "/evaluations/empty_run/results?limit=100_000"
    )
    assert result == []


def test_list_entries_run_not_found(evaluations_resource, mock_client):
    """Test list_entries with non-existent run ID."""
    mock_client.get.side_effect = HubAPIError(
        "Evaluation run not found", status_code=404
    )

    with pytest.raises(HubAPIError) as exc_info:
        evaluations_resource.list_entries("nonexistent_run")

    assert exc_info.value.status_code == 404


def test_list_entries_json_decode_error(evaluations_resource, mock_client):
    """Test list_entries with JSON decode error."""
    mock_client.get.side_effect = HubJSONDecodeError(
        "Invalid JSON response", status_code=200
    )

    with pytest.raises(HubJSONDecodeError):
        evaluations_resource.list_entries("run_123")


def test_list_entries_with_failure_categories(evaluations_resource, mock_client):
    """Test successful listing of evaluation entries with failure categories."""
    mock_response = {
        "items": [
            TEST_EVALUATION_ENTRY_DATA,
            TEST_EVALUATION_ENTRY_WITH_FAILURE_CATEGORY,
        ]
    }
    mock_client.get.return_value = mock_response

    result = evaluations_resource.list_entries("run_123")

    mock_client.get.assert_called_once_with(
        "/evaluations/run_123/results?limit=100_000"
    )
    assert len(result) == 2
    assert all(isinstance(entry, EvaluationEntry) for entry in result)

    # Test first entry without failure category
    assert result[0].failure_category is None

    # Test second entry with failure category
    assert result[1].failure_category is not None
    assert result[1].failure_category.category is not None
    assert result[1].failure_category.category.identifier == "hallucination"
    assert result[1].failure_category.category.title == "Hallucination"
    assert (
        result[1].failure_category.category.description
        == "Model generated false or misleading information"
    )
    assert result[1].failure_category.status == TaskStatus.FINISHED
    assert result[1].failure_category.error is None


def test_list_entries_with_failure_category_error(evaluations_resource, mock_client):
    """Test listing entries with failure category that has an error."""
    failure_category_with_error = {
        "category": TEST_FAILURE_CATEGORY_DATA,
        "status": "error",
        "error": "Failed to categorize: timeout error",
    }

    entry_with_error = TEST_EVALUATION_ENTRY_DATA.copy()
    entry_with_error["failure_category"] = failure_category_with_error

    mock_response = {"items": [entry_with_error]}
    mock_client.get.return_value = mock_response

    result = evaluations_resource.list_entries("run_123")

    assert len(result) == 1
    entry = result[0]
    assert entry.failure_category is not None
    assert entry.failure_category.category is not None
    assert entry.failure_category.category.identifier == "hallucination"
    assert entry.failure_category.status == TaskStatus.ERROR
    assert entry.failure_category.error == "Failed to categorize: timeout error"


def test_list_entries_with_null_failure_category(evaluations_resource, mock_client):
    """Test listing entries with null failure category."""
    entry_with_null_category = TEST_EVALUATION_ENTRY_DATA.copy()
    entry_with_null_category["failure_category"] = {
        "category": None,
        "status": None,
        "error": "No category assigned",
    }

    mock_response = {"items": [entry_with_null_category]}
    mock_client.get.return_value = mock_response

    result = evaluations_resource.list_entries("run_123")

    assert len(result) == 1
    entry = result[0]
    assert entry.failure_category is not None
    assert entry.failure_category.category is None
    assert entry.failure_category.status is None
    assert entry.failure_category.error == "No category assigned"


# Tests for EvaluationsResource.update_entry()
def test_update_entry_with_model_output_success(evaluations_resource, mock_client):
    """Test successful update of entry with model output."""
    mock_client.patch.return_value = TEST_EVALUATION_ENTRY_DATA
    model_output = ModelOutput.from_dict(TEST_MODEL_OUTPUT_DATA)

    result = evaluations_resource.update_entry(
        run_id="run_123", entry_id="entry_456", model_output=model_output
    )

    expected_data = {
        "output": {
            "response": model_output.message.to_dict(),
            "metadata": model_output.metadata,
        }
    }

    mock_client.patch.assert_called_once_with(
        "/evaluations/run_123/results/entry_456/submit-local",
        json=expected_data,
        cast_to=EvaluationEntry,
    )
    assert result == TEST_EVALUATION_ENTRY_DATA


def test_update_entry_with_results_success(evaluations_resource, mock_client):
    """Test successful update of entry with evaluator results."""
    mock_client.patch.return_value = TEST_EVALUATION_ENTRY_DATA
    results = [EvaluatorResult.from_dict(r) for r in TEST_EVALUATOR_RESULTS]

    result = evaluations_resource.update_entry(
        run_id="run_123", entry_id="entry_456", results=results
    )

    expected_data = {"results": [r.to_dict() for r in results]}

    mock_client.patch.assert_called_once_with(
        "/evaluations/run_123/results/entry_456/submit-local",
        json=expected_data,
        cast_to=EvaluationEntry,
    )
    assert result == TEST_EVALUATION_ENTRY_DATA


def test_update_entry_with_both_params(evaluations_resource, mock_client):
    """Test successful update of entry with both model output and results."""
    mock_client.patch.return_value = TEST_EVALUATION_ENTRY_DATA
    model_output = ModelOutput.from_dict(TEST_MODEL_OUTPUT_DATA)
    results = [EvaluatorResult.from_dict(r) for r in TEST_EVALUATOR_RESULTS]

    result = evaluations_resource.update_entry(
        run_id="run_123",
        entry_id="entry_456",
        model_output=model_output,
        results=results,
    )

    expected_data = {
        "output": {
            "response": model_output.message.to_dict(),
            "metadata": model_output.metadata,
        },
        "results": [r.to_dict() for r in results],
    }

    mock_client.patch.assert_called_once_with(
        "/evaluations/run_123/results/entry_456/submit-local",
        json=expected_data,
        cast_to=EvaluationEntry,
    )
    assert result == TEST_EVALUATION_ENTRY_DATA


def test_update_entry_with_dict_model_output(evaluations_resource, mock_client):
    """Test update entry with model output as dictionary (auto-conversion)."""
    mock_client.patch.return_value = TEST_EVALUATION_ENTRY_DATA

    result = evaluations_resource.update_entry(
        run_id="run_123",
        entry_id="entry_456",
        model_output=TEST_MODEL_OUTPUT_DATA,  # Pass as dict, should be converted
    )

    # Should convert dict to ModelOutput and then extract the data
    model_output = ModelOutput.from_dict(TEST_MODEL_OUTPUT_DATA)
    expected_data = {
        "output": {
            "response": model_output.message.to_dict(),
            "metadata": model_output.metadata,
        }
    }

    mock_client.patch.assert_called_once_with(
        "/evaluations/run_123/results/entry_456/submit-local",
        json=expected_data,
        cast_to=EvaluationEntry,
    )
    assert result == TEST_EVALUATION_ENTRY_DATA


def test_update_entry_no_params(evaluations_resource, mock_client):
    """Test update entry with no parameters (should send empty data)."""
    mock_client.patch.return_value = TEST_EVALUATION_ENTRY_DATA

    result = evaluations_resource.update_entry(run_id="run_123", entry_id="entry_456")

    expected_data = {}

    mock_client.patch.assert_called_once_with(
        "/evaluations/run_123/results/entry_456/submit-local",
        json=expected_data,
        cast_to=EvaluationEntry,
    )
    assert result == TEST_EVALUATION_ENTRY_DATA


def test_update_entry_validation_error(evaluations_resource, mock_client):
    """Test update entry with validation error."""
    mock_client.patch.side_effect = HubValidationError(
        "Validation failed: invalid entry data", status_code=422
    )

    with pytest.raises(HubValidationError) as exc_info:
        evaluations_resource.update_entry(
            run_id="run_123",
            entry_id="invalid_entry",
            model_output=ModelOutput.from_dict(TEST_MODEL_OUTPUT_DATA),
        )

    assert exc_info.value.status_code == 422


def test_update_entry_not_found(evaluations_resource, mock_client):
    """Test update entry with non-existent entry ID."""
    mock_client.patch.side_effect = HubAPIError("Entry not found", status_code=404)

    with pytest.raises(HubAPIError) as exc_info:
        evaluations_resource.update_entry(
            run_id="run_123",
            entry_id="nonexistent_entry",
            model_output=ModelOutput.from_dict(TEST_MODEL_OUTPUT_DATA),
        )

    assert exc_info.value.status_code == 404


def test_update_entry_forbidden(evaluations_resource, mock_client):
    """Test update entry with forbidden access."""
    mock_client.patch.side_effect = HubForbiddenError(
        "Cannot update entry", status_code=403
    )

    with pytest.raises(HubForbiddenError):
        evaluations_resource.update_entry(
            run_id="run_123",
            entry_id="entry_456",
            model_output=ModelOutput.from_dict(TEST_MODEL_OUTPUT_DATA),
        )
