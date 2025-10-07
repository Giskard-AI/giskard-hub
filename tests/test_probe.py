import uuid
from unittest.mock import MagicMock

import pytest

from giskard_hub.data.scan import ProbeAttempt, ProbeResult, ReviewStatus, Severity
from giskard_hub.data.task import TaskStatus


class TestProbeAttempt:
    """Test the ProbeAttempt data model."""

    def test_probe_attempt_from_dict_full(self):
        attempt_id = str(uuid.uuid4())
        probe_result_id = str(uuid.uuid4())
        data = {
            "id": attempt_id,
            "probe_result_id": probe_result_id,
            "messages": [
                {
                    "role": "user",
                    "content": "What is the issue?",
                    "metadata": {"timestamp": "2025-10-06T12:00:00Z"},
                },
                {
                    "role": "assistant",
                    "content": "The model is biased.",
                    "metadata": {"timestamp": "2025-10-06T12:05:00Z"},
                },
            ],
            "metadata": {"attempt_number": 1},
            "severity": 20,
            "review_status": ReviewStatus.ACKNOWLEDGED.value,
            "reason": "Detected bias in predictions",
            "error": {
                "message": "No error",
            },
        }
        attempt = ProbeAttempt.from_dict(data)
        assert attempt.id == attempt_id
        assert attempt.probe_result_id == probe_result_id
        assert len(attempt.messages) == 2
        assert attempt.messages[0].role == "user"
        assert attempt.messages[0].content == "What is the issue?"
        assert attempt.messages[0].metadata["timestamp"] == "2025-10-06T12:00:00Z"
        assert attempt.messages[1].role == "assistant"
        assert attempt.messages[1].content == "The model is biased."
        assert attempt.messages[1].metadata["timestamp"] == "2025-10-06T12:05:00Z"
        assert attempt.metadata["attempt_number"] == 1
        assert attempt.severity == 20
        assert attempt.review_status == ReviewStatus.ACKNOWLEDGED
        assert attempt.reason == "Detected bias in predictions"
        assert attempt.error is not None
        assert attempt.error.message == "No error"

    def test_probe_attempt_from_dict_minimal(self):
        attempt_id = str(uuid.uuid4())
        probe_result_id = str(uuid.uuid4())
        data = {
            "id": attempt_id,
            "probe_result_id": probe_result_id,
            "messages": [],
            "metadata": {},
            "severity": Severity.SAFE.value,
            "review_status": ReviewStatus.ACKNOWLEDGED.value,
            "reason": "Initial attempt",
        }
        attempt = ProbeAttempt.from_dict(data)
        assert attempt.id == attempt_id
        assert attempt.probe_result_id == probe_result_id
        assert attempt.messages == []
        assert attempt.metadata == {}
        assert attempt.severity == Severity.SAFE
        assert attempt.review_status == ReviewStatus.ACKNOWLEDGED
        assert attempt.reason == "Initial attempt"
        assert attempt.error is None


@pytest.fixture
def mock_client():
    """Mock client for testing data model."""

    mock_client = MagicMock()
    mock_client.probes.get_attempts.return_value = [
        ProbeAttempt.from_dict(a)
        for a in [
            {
                "id": str(uuid.uuid4()),
                "probe_result_id": str(uuid.uuid4()),
                "messages": [],
                "metadata": {},
                "severity": Severity.MINOR.value,
                "review_status": ReviewStatus.PENDING.value,
                "reason": "Mock attempt",
            },
        ]
    ]
    return mock_client


class TestProbeResult:
    """Test the ProbeResult data model."""

    def test_probe_result_from_dict_full(self):
        probe_result_id = str(uuid.uuid4())
        scan_result_id = str(uuid.uuid4())
        data = {
            "id": probe_result_id,
            "scan_result_id": scan_result_id,
            "probe_lidar_id": "lidar-123",
            "probe_name": "Bias Detection Probe",
            "probe_description": "Detects bias in model predictions",
            "probe_tags": ["bias", "fairness"],
            "probe_category": "Fairness",
            "metrics": [
                {
                    "severity": Severity.SAFE.value,
                    "count": 1,
                },
                {
                    "severity": Severity.MINOR.value,
                    "count": 2,
                },
            ],
            "status": {
                "state": TaskStatus.FINISHED.value,
                "current": 100,
                "total": 100,
                "error": None,
            },
        }
        probe_result = ProbeResult.from_dict(data)
        assert probe_result.id == probe_result_id
        assert probe_result.scan_result_id == scan_result_id
        assert probe_result.probe_lidar_id == "lidar-123"
        assert probe_result.probe_name == "Bias Detection Probe"
        assert probe_result.probe_description == "Detects bias in model predictions"
        assert probe_result.probe_tags == ["bias", "fairness"]
        assert probe_result.probe_category == "Fairness"
        assert len(probe_result.metrics) == 2
        assert probe_result.metrics[0].severity == Severity.SAFE
        assert probe_result.metrics[0].count == 1
        assert probe_result.metrics[1].severity == Severity.MINOR
        assert probe_result.metrics[1].count == 2
        assert probe_result.progress is not None
        assert probe_result.progress.status == TaskStatus.FINISHED
        assert probe_result.progress.current == 100
        assert probe_result.progress.total == 100
        assert probe_result.progress.error is None

    def test_probe_result_from_dict_minimal(self):
        probe_result_id = str(uuid.uuid4())
        scan_result_id = str(uuid.uuid4())
        data = {
            "id": probe_result_id,
            "scan_result_id": scan_result_id,
            "probe_lidar_id": "lidar-123",
            "probe_name": "Minimal Probe",
            "probe_description": "A minimal probe description",
            "probe_tags": [],
            "probe_category": "General",
        }
        probe_result = ProbeResult.from_dict(data)
        assert probe_result.id == probe_result_id
        assert probe_result.scan_result_id == scan_result_id
        assert probe_result.probe_lidar_id == "lidar-123"
        assert probe_result.probe_name == "Minimal Probe"
        assert probe_result.probe_description == "A minimal probe description"
        assert probe_result.probe_tags == []
        assert probe_result.probe_category == "General"
        assert probe_result.metrics is None
        assert probe_result.progress is None

    def test_probe_result_attempts(self, mock_client):
        probe_result_id = str(uuid.uuid4())
        probe_result = ProbeResult.from_dict(
            {
                "id": probe_result_id,
                "scan_result_id": str(uuid.uuid4()),
                "probe_lidar_id": "lidar-123",
                "probe_name": "Test Probe",
                "probe_description": "Testing attempts",
                "probe_tags": [],
                "probe_category": "Test",
            },
            _client=mock_client,
        )
        attempts = probe_result.attempts

        mock_client.probes.get_attempts.assert_called_once()

        assert isinstance(attempts, list)
        assert len(attempts) == 1
        attempt = attempts[0]
        assert isinstance(attempt, ProbeAttempt)
        assert attempt.reason == "Mock attempt"
        assert attempt.severity == Severity.MINOR
        assert attempt.review_status == ReviewStatus.PENDING


@pytest.fixture
def mock_http_client():
    """Mock HTTP client for testing API resources."""
    mock_client = MagicMock()

    def handle_get_response(path, cast_to=None, **kwargs):
        response_data = mock_client.get.return_value
        if cast_to is None:
            return response_data

        if cast_to == ProbeAttempt:
            return ProbeAttempt.from_dict(response_data)
        elif cast_to == ProbeResult:
            return ProbeResult.from_dict(response_data)

        return response_data

    # Only GET is used in probe routes
    mock_client.get.side_effect = handle_get_response

    return mock_client


class TestProbeResultResource:
    """Test the Probe API resources."""

    def test_probe_resource_retrieve(self, mock_http_client):
        pass

    def test_probe_resource_get_attempts(self, mock_http_client):
        pass

