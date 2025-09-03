from datetime import datetime
from unittest.mock import MagicMock

import pytest

from giskard_hub.data.scheduled_evaluation import (
    ErrorExecutionStatus,
    FrequencyOption,
    ScheduledEvaluation,
    SuccessExecutionStatus,
)
from giskard_hub.errors import HubValidationError
from giskard_hub.resources.scheduled_evaluations import ScheduledEvaluationsResource


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
            if cast_to == ScheduledEvaluation:
                return [
                    ScheduledEvaluation.from_dict(item, _client=mock_client)
                    for item in response_data
                ]
        else:
            if cast_to == ScheduledEvaluation:
                return ScheduledEvaluation.from_dict(response_data, _client=mock_client)

        return response_data

    # GET
    mock_client.get.side_effect = handle_get_response

    # POST
    mock_client.post.side_effect = lambda path, cast_to=None, **kwargs: (
        ScheduledEvaluation.from_dict(
            mock_client.post.return_value, _client=mock_client
        )
        if cast_to == ScheduledEvaluation
        else mock_client.post.return_value
    )

    # PATCH
    mock_client.patch.side_effect = lambda path, cast_to=None, **kwargs: (
        ScheduledEvaluation.from_dict(
            mock_client.patch.return_value, _client=mock_client
        )
        if cast_to == ScheduledEvaluation
        else mock_client.patch.return_value
    )

    # DELETE
    mock_client.delete.side_effect = lambda path, **kwargs: None

    return mock_client


class TestScheduledEvaluationsResource:
    """Test the ScheduledEvaluationsResource class."""

    def test_list(self, mock_client):
        """Test listing scheduled evaluations."""
        resource = ScheduledEvaluationsResource(mock_client)

        # Mock the response
        mock_scheduled_evals_data = [
            {
                "id": "se1",
                "project_id": "project-id",
                "name": "Daily Evaluation",
                "model_id": "model-1",
                "dataset_id": "dataset-1",
                "frequency": "daily",
                "time": "09:00",
                "run_count": 1,
                "tags": [],
                "paused": False,
            },
            {
                "id": "se2",
                "project_id": "project-id",
                "name": "Weekly Evaluation",
                "model_id": "model-2",
                "dataset_id": "dataset-2",
                "frequency": "weekly",
                "time": "10:30",
                "day_of_week": 1,
                "run_count": 3,
                "tags": ["production"],
                "paused": True,
            },
        ]
        mock_client.get.return_value = mock_scheduled_evals_data

        result = resource.list(project_id="project-id")

        mock_client.get.assert_called_once_with(
            "/scheduled-evaluations",
            params={"project_id": "project-id"},
        )
        assert len(result) == 2
        assert result[0].id == "se1"
        assert result[0].name == "Daily Evaluation"
        assert result[0].frequency == FrequencyOption.DAILY
        assert result[1].id == "se2"
        assert result[1].name == "Weekly Evaluation"
        assert result[1].frequency == FrequencyOption.WEEKLY

    def test_retrieve(self, mock_client):
        """Test retrieving a scheduled evaluation."""
        resource = ScheduledEvaluationsResource(mock_client)

        # Mock the response
        mock_scheduled_eval_data = {
            "id": "se1",
            "project_id": "project-id",
            "name": "Test Evaluation",
            "model_id": "model-1",
            "dataset_id": "dataset-1",
            "frequency": "daily",
            "time": "14:30",
            "run_count": 2,
            "tags": ["test", "automated"],
            "paused": False,
            "last_execution_at": "2023-10-15T14:30:00Z",
            "last_execution_status": {"status": "success", "evaluation_id": "eval-123"},
        }
        mock_client.get.return_value = mock_scheduled_eval_data

        result = resource.retrieve("se1")

        mock_client.get.assert_called_once_with(
            "/scheduled-evaluations/se1", cast_to=ScheduledEvaluation
        )
        assert result.id == "se1"
        assert result.name == "Test Evaluation"
        assert result.run_count == 2
        assert result.tags == ["test", "automated"]
        assert isinstance(result.last_execution_status, SuccessExecutionStatus)
        assert result.last_execution_status.evaluation_id == "eval-123"

    def test_retrieve_with_error_status(self, mock_client):
        """Test retrieving a scheduled evaluation with error status."""
        resource = ScheduledEvaluationsResource(mock_client)

        # Mock the response
        mock_scheduled_eval_data = {
            "id": "se1",
            "project_id": "project-id",
            "name": "Failed Evaluation",
            "model_id": "model-1",
            "dataset_id": "dataset-1",
            "frequency": "daily",
            "time": "14:30",
            "run_count": 1,
            "tags": [],
            "paused": False,
            "last_execution_at": "2023-10-15T14:30:00Z",
            "last_execution_status": {
                "status": "error",
                "error_message": "Model endpoint unavailable",
            },
        }
        mock_client.get.return_value = mock_scheduled_eval_data

        result = resource.retrieve("se1")

        assert isinstance(result.last_execution_status, ErrorExecutionStatus)
        assert (
            result.last_execution_status.error_message == "Model endpoint unavailable"
        )

    def test_create_daily(self, mock_client):
        """Test creating a daily scheduled evaluation."""
        resource = ScheduledEvaluationsResource(mock_client)

        # Mock the response
        mock_created_data = {
            "id": "se-new",
            "project_id": "project-id",
            "name": "New Daily Evaluation",
            "model_id": "model-1",
            "dataset_id": "dataset-1",
            "frequency": "daily",
            "time": "08:00",
            "run_count": 1,
            "tags": [],
            "paused": False,
        }
        mock_client.post.return_value = mock_created_data

        result = resource.create(
            project_id="project-id",
            name="New Daily Evaluation",
            model_id="model-1",
            dataset_id="dataset-1",
            frequency="daily",
            time="08:00",
        )

        mock_client.post.assert_called_once()
        call_args = mock_client.post.call_args
        assert call_args[0][0] == "/scheduled-evaluations"
        assert call_args[1]["json"]["project_id"] == "project-id"
        assert call_args[1]["json"]["name"] == "New Daily Evaluation"
        assert call_args[1]["json"]["frequency"] == "daily"
        assert call_args[1]["json"]["time"] == "08:00"
        assert call_args[1]["cast_to"] == ScheduledEvaluation
        assert result.id == "se-new"

    def test_create_weekly_with_options(self, mock_client):
        """Test creating a weekly scheduled evaluation with optional parameters."""
        resource = ScheduledEvaluationsResource(mock_client)

        # Mock the response
        mock_created_data = {
            "id": "se-weekly",
            "project_id": "project-id",
            "name": "Weekly Evaluation",
            "model_id": "model-2",
            "dataset_id": "dataset-2",
            "frequency": "weekly",
            "time": "12:00",
            "day_of_week": 5,
            "run_count": 3,
            "tags": ["production", "weekly"],
            "paused": False,
        }
        mock_client.post.return_value = mock_created_data

        resource.create(
            project_id="project-id",
            name="Weekly Evaluation",
            model_id="model-2",
            dataset_id="dataset-2",
            frequency="weekly",
            time="12:00",
            day_of_week=5,
            run_count=3,
            tags=["production", "weekly"],
        )

        call_args = mock_client.post.call_args
        assert call_args[1]["json"]["day_of_week"] == 5
        assert call_args[1]["json"]["run_count"] == 3
        assert call_args[1]["json"]["tags"] == ["production", "weekly"]

    def test_create_monthly(self, mock_client):
        """Test creating a monthly scheduled evaluation."""
        resource = ScheduledEvaluationsResource(mock_client)

        # Mock the response
        mock_created_data = {
            "id": "se-monthly",
            "project_id": "project-id",
            "name": "Monthly Evaluation",
            "model_id": "model-3",
            "dataset_id": "dataset-3",
            "frequency": "monthly",
            "time": "00:00",
            "day_of_month": 15,
            "run_count": 1,
            "tags": [],
            "paused": False,
        }
        mock_client.post.return_value = mock_created_data

        resource.create(
            project_id="project-id",
            name="Monthly Evaluation",
            model_id="model-3",
            dataset_id="dataset-3",
            frequency="monthly",
            time="00:00",
            day_of_month=15,
        )

        call_args = mock_client.post.call_args
        assert call_args[1]["json"]["day_of_month"] == 15

    def test_create_daily_with_day_of_week_warning(self, mock_client):
        """Test creating a daily scheduled evaluation with day_of_week parameter (should warn)."""
        resource = ScheduledEvaluationsResource(mock_client)

        # Mock the response
        mock_created_data = {
            "id": "se-daily-warn",
            "project_id": "project-id",
            "name": "Daily Evaluation with Warning",
            "model_id": "model-1",
            "dataset_id": "dataset-1",
            "frequency": "daily",
            "time": "10:00",
            "run_count": 1,
            "tags": [],
            "paused": False,
        }
        mock_client.post.return_value = mock_created_data

        # Test that it works but issues a warning
        with pytest.warns(
            UserWarning,
            match="day_of_week and day_of_month are ignored when frequency is 'daily'",
        ):
            result = resource.create(
                project_id="project-id",
                name="Daily Evaluation with Warning",
                model_id="model-1",
                dataset_id="dataset-1",
                frequency="daily",
                time="10:00",
                day_of_week=1,  # This should trigger a warning but not fail
            )

        # Verify the call was made successfully
        mock_client.post.assert_called_once()
        call_args = mock_client.post.call_args
        assert call_args[1]["json"]["frequency"] == "daily"
        assert call_args[1]["json"]["day_of_week"] == 1  # Parameter is still passed
        assert result.id == "se-daily-warn"

    def test_create_weekly_with_day_of_month_error(self, mock_client):
        """Test creating a weekly scheduled evaluation with day_of_month parameter (should error)."""
        resource = ScheduledEvaluationsResource(mock_client)

        # Test that it raises an error because day_of_week is required for weekly frequency
        with pytest.raises(
            HubValidationError,
            match="day_of_week must be provided when frequency is 'weekly'",
        ):
            resource.create(
                project_id="project-id",
                name="Weekly Evaluation Error",
                model_id="model-2",
                dataset_id="dataset-2",
                frequency="weekly",
                time="12:00",
                day_of_month=1,  # Wrong parameter for weekly frequency
            )

        # Verify no API call was made due to validation error
        mock_client.post.assert_not_called()

    def test_create_monthly_with_day_of_week_error(self, mock_client):
        """Test creating a monthly scheduled evaluation with day_of_week parameter (should error)."""
        resource = ScheduledEvaluationsResource(mock_client)

        # Test that it raises an error because day_of_month is required for monthly frequency
        with pytest.raises(
            HubValidationError,
            match="day_of_month must be provided when frequency is 'monthly'",
        ):
            resource.create(
                project_id="project-id",
                name="Monthly Evaluation Error",
                model_id="model-3",
                dataset_id="dataset-3",
                frequency="monthly",
                time="00:00",
                day_of_week=1,  # Wrong parameter for monthly frequency
            )

        # Verify no API call was made due to validation error
        mock_client.post.assert_not_called()

    def test_update(self, mock_client):
        """Test updating a scheduled evaluation."""
        resource = ScheduledEvaluationsResource(mock_client)

        # Mock the response
        mock_updated_data = {
            "id": "se1",
            "project_id": "project-id",
            "name": "Updated Evaluation Name",
            "model_id": "model-1",
            "dataset_id": "dataset-1",
            "frequency": "weekly",
            "time": "16:00",
            "day_of_week": 3,
            "run_count": 2,
            "tags": ["test-tag"],
            "paused": True,
        }
        mock_client.patch.return_value = mock_updated_data

        result = resource.update(
            "se1",
            name="Updated Evaluation Name",
            frequency="weekly",
            time="16:00",
            day_of_week=3,
            run_count=2,
            paused=True,
        )

        mock_client.patch.assert_called_once()
        call_args = mock_client.patch.call_args
        assert call_args[0][0] == "/scheduled-evaluations/se1"
        json_data = call_args[1]["json"]
        assert json_data["name"] == "Updated Evaluation Name"
        assert json_data["frequency"] == "weekly"
        assert json_data["time"] == "16:00"
        assert json_data["day_of_week"] == 3
        assert json_data["run_count"] == 2
        assert json_data["paused"] is True
        assert result.name == "Updated Evaluation Name"

    def test_update_partial(self, mock_client):
        """Test partial update of a scheduled evaluation."""
        resource = ScheduledEvaluationsResource(mock_client)

        # Mock the response
        mock_updated_data = {
            "id": "se1",
            "project_id": "project-id",
            "name": "Original Name",
            "model_id": "model-1",
            "dataset_id": "dataset-1",
            "frequency": "daily",
            "time": "08:00",
            "run_count": 1,
            "tags": [],
            "paused": True,  # Only this should be updated
        }
        mock_client.patch.return_value = mock_updated_data

        resource.update("se1", paused=True)

        call_args = mock_client.patch.call_args
        json_data = call_args[1]["json"]
        # Only paused should be in the payload
        assert json_data == {"paused": True}

    def test_delete_single(self, mock_client):
        """Test deleting a single scheduled evaluation."""
        resource = ScheduledEvaluationsResource(mock_client)

        resource.delete(["se1"])

        mock_client.delete.assert_called_once_with(
            "/scheduled-evaluations",
            params={"scheduled_evaluation_ids": ["se1"]},
        )

    def test_delete_multiple(self, mock_client):
        """Test deleting multiple scheduled evaluations."""
        resource = ScheduledEvaluationsResource(mock_client)

        resource.delete(["se1", "se2", "se3"])

        mock_client.delete.assert_called_once_with(
            "/scheduled-evaluations",
            params={"scheduled_evaluation_ids": ["se1", "se2", "se3"]},
        )


class TestScheduledEvaluationDataModel:
    """Test the ScheduledEvaluation data model."""

    def test_scheduled_evaluation_from_dict_basic(self):
        """Test creating ScheduledEvaluation from basic dict."""
        data = {
            "id": "se1",
            "project_id": "project-id",
            "name": "Test Evaluation",
            "model_id": "model-1",
            "dataset_id": "dataset-1",
            "frequency": "daily",
            "time": "09:00",
            "run_count": 1,
            "tags": [],
            "paused": False,
        }

        result = ScheduledEvaluation.from_dict(data)

        assert result.id == "se1"
        assert result.name == "Test Evaluation"
        assert result.frequency == FrequencyOption.DAILY
        assert result.time == "09:00"
        assert result.run_count == 1
        assert result.paused is False

    def test_scheduled_evaluation_from_dict_with_success_status(self):
        """Test creating ScheduledEvaluation with success execution status."""
        data = {
            "id": "se1",
            "project_id": "project-id",
            "name": "Test Evaluation",
            "model_id": "model-1",
            "dataset_id": "dataset-1",
            "frequency": "daily",
            "time": "09:00",
            "run_count": 1,
            "tags": [],
            "paused": False,
            "last_execution_at": "2023-10-15T14:30:00Z",
            "last_execution_status": {"status": "success", "evaluation_id": "eval-123"},
        }

        result = ScheduledEvaluation.from_dict(data)

        assert isinstance(result.last_execution_status, SuccessExecutionStatus)
        assert result.last_execution_status.evaluation_id == "eval-123"
        assert result.last_execution_status.status == "success"
        assert isinstance(result.last_execution_at, datetime)

    def test_scheduled_evaluation_from_dict_with_error_status(self):
        """Test creating ScheduledEvaluation with error execution status."""
        data = {
            "id": "se1",
            "project_id": "project-id",
            "name": "Test Evaluation",
            "model_id": "model-1",
            "dataset_id": "dataset-1",
            "frequency": "daily",
            "time": "09:00",
            "run_count": 1,
            "tags": [],
            "paused": False,
            "last_execution_at": "2023-10-15T14:30:00Z",
            "last_execution_status": {
                "status": "error",
                "error_message": "Model endpoint unavailable",
            },
        }

        result = ScheduledEvaluation.from_dict(data)

        assert isinstance(result.last_execution_status, ErrorExecutionStatus)
        assert (
            result.last_execution_status.error_message == "Model endpoint unavailable"
        )
        assert result.last_execution_status.status == "error"


class TestExecutionStatus:
    """Test the execution status classes."""

    def test_success_execution_status_from_dict(self):
        """Test creating SuccessExecutionStatus from dict."""
        data = {"status": "success", "evaluation_id": "eval-123"}

        result = SuccessExecutionStatus.from_dict(data)

        assert result.status == "success"
        assert result.evaluation_id == "eval-123"

    def test_error_execution_status_from_dict(self):
        """Test creating ErrorExecutionStatus from dict."""
        data = {"status": "error", "error_message": "Connection timeout"}

        result = ErrorExecutionStatus.from_dict(data)

        assert result.status == "error"
        assert result.error_message == "Connection timeout"

    def test_frequency_option_enum(self):
        """Test FrequencyOption enum values."""
        assert FrequencyOption.DAILY == "daily"
        assert FrequencyOption.WEEKLY == "weekly"
        assert FrequencyOption.MONTHLY == "monthly"
