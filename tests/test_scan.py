import uuid
from unittest.mock import MagicMock

import pytest

from giskard_hub.data.scan import ProbeResult, ScanGrade, ScanResult, ScanType
from giskard_hub.data.task import TaskStatus

_TEST_PROBE_ID = str(uuid.uuid4())
_TEST_SCAN_ID = str(uuid.uuid4())
_TEST_PROJECT_ID = str(uuid.uuid4())
_TEST_MODEL_ID = str(uuid.uuid4())


@pytest.fixture
def mock_client():
    """Mock client for testing."""
    mock_client = MagicMock()

    # GET /scans/{scan_id}/probes to get probe results for a scan
    test_probe = {
        "id": _TEST_PROBE_ID,
        "scan_result_id": _TEST_SCAN_ID,
        "probe_lidar_id": "probe_1",
        "probe_name": "Test Probe",
        "probe_description": "A test probe",
        "probe_tags": ["tag1", "tag2"],
        "probe_category": "Category A",
        "metrics": [],
        "status": {
            "state": "finished",
            "total": 100,
            "current": 100,
        },
    }
    mock_client.scans.get_probes.return_value = [
        ProbeResult.from_dict(r, _client=mock_client)
        for r in [
            test_probe,
        ]
    ]

    test_scan = {
        "id": _TEST_SCAN_ID,
        "project_id": _TEST_PROJECT_ID,
        "model": {"id": _TEST_MODEL_ID, "name": "Test Model"},
        "status": {
            "state": "finished",
            "total": 100,
            "current": 100,
        },
        "start_datetime": "2023-10-01T12:00:00Z",
        "end_datetime": "2023-10-01T13:00:00Z",
        "grade": ScanGrade.A.value,
        "lidar_version": "1.0.0",
        "tags": ["tag1", "tag2"],
        "scan_type": ScanType.IN_DEPTH.value,
        "errors": [],
        "generator_metadata": {},
        "target_info": {},
        "scan_metadata": {},
    }
    # GET /scans/{scan_id} to retrieve a specific scan
    mock_client.scans.retrieve.return_value = ScanResult.from_dict(
        test_scan, _client=mock_client
    )

    return mock_client


class TestScanResultDataModel:
    """Test the Scan data model."""

    def test_scan_result_from_dict_basic(self):
        scan_id = str(uuid.uuid4())
        project_id = str(uuid.uuid4())
        model_id = str(uuid.uuid4())
        scan_dict = {
            "id": scan_id,
            "project_id": project_id,
            "model": {"id": model_id, "name": "Test Model"},
            "status": {
                "state": "finished",
                "total": 100,
                "current": 100,
            },
            "start_datetime": "2023-10-01T12:00:00Z",
            "end_datetime": "2023-10-01T13:00:00Z",
            "grade": ScanGrade.A.value,
            "lidar_version": "1.0.0",
            "tags": ["tag1", "tag2"],
            "scan_type": ScanType.IN_DEPTH.value,
            "errors": [],
            "generator_metadata": {},
            "target_info": {},
            "scan_metadata": {},
        }

        scan = ScanResult.from_dict(scan_dict)

        assert scan.id == scan_id
        assert scan.project_id == project_id
        assert scan.model.id == model_id
        assert scan.model.name == "Test Model"
        assert scan.progress.status == TaskStatus.FINISHED
        assert scan.progress.total == 100
        assert scan.progress.current == 100
        assert scan.start_datetime.isoformat() == "2023-10-01T12:00:00+00:00"
        assert scan.grade == ScanGrade.A
        assert scan.lidar_version == "1.0.0"
        assert scan.tags == ["tag1", "tag2"]
        assert scan.scan_type == ScanType.IN_DEPTH
        assert scan.errors == []
        assert scan.generator_metadata == {}
        assert scan.target_info == {}
        assert scan.scan_metadata == {}

    def test_scan_result_from_dict_minimal(self):
        scan_id = str(uuid.uuid4())
        project_id = str(uuid.uuid4())
        model_id = str(uuid.uuid4())
        scan_dict = {
            "id": scan_id,
            "project_id": project_id,
            "model": {"id": model_id, "name": "Minimal Model"},
        }

        scan = ScanResult.from_dict(scan_dict)

        assert scan.id == scan_id
        assert scan.model.id == model_id
        assert scan.model.name == "Minimal Model"
        assert scan.project_id == project_id
        assert scan.progress is None
        assert scan.grade is None
        assert scan.lidar_version == None  # from_dict doesn't populate defaults
        assert scan.tags == None  # from_dict doesn't populate defaults
        assert scan.scan_type == None  # from_dict doesn't populate defaults
        assert scan.errors == None  # from_dict doesn't populate defaults
        assert scan.generator_metadata == None  # from_dict doesn't populate defaults
        assert scan.target_info == None  # from_dict doesn't populate defaults
        assert scan.scan_metadata == None  # from_dict doesn't populate defaults

    def test_scan_result_from_dict_with_errors(self):
        scan_id = str(uuid.uuid4())
        project_id = str(uuid.uuid4())
        model_id = str(uuid.uuid4())
        scan_dict = {
            "id": scan_id,
            "project_id": project_id,
            "model": {"id": model_id, "name": "Error Model"},
            "status": {
                "state": "error",
                "total": 100,
                "current": 50,
                "error": "An error occurred",
            },
            "errors": [
                {
                    "probe_lidar_id": "probe_1",
                    "original_error": "Original error message",
                    "trace": "Trace details here",
                }
            ],
            "scan_type": ScanType.IN_DEPTH.value,
            "generator_metadata": {},
            "target_info": {},
            "scan_metadata": {},
        }

        scan = ScanResult.from_dict(scan_dict)

        assert scan.id == scan_id
        assert scan.model.id == model_id
        assert scan.model.name == "Error Model"
        assert scan.project_id == project_id
        assert scan.progress.status == TaskStatus.ERROR
        assert scan.progress.total == 100
        assert scan.progress.current == 50
        assert scan.progress.error == "An error occurred"
        assert len(scan.errors) == 1
        assert scan.errors[0].probe_lidar_id == "probe_1"
        assert scan.errors[0].original_error == "Original error message"
        assert scan.errors[0].trace == "Trace details here"
        assert scan.scan_type == ScanType.IN_DEPTH
        assert scan.generator_metadata == {}
        assert scan.target_info == {}
        assert scan.scan_metadata == {}

    def test_scan_result_get_probe_results(self, mock_client):
        scan = ScanResult.from_dict(
            {
                "id": _TEST_SCAN_ID,
                "project_id": _TEST_PROJECT_ID,
                "model": {"id": _TEST_MODEL_ID, "name": "Probe Model"},
            },
            _client=mock_client,
        )

        results = scan.results
        mock_client.scans.get_probes.assert_called_once()
        assert len(results) == 1

        result = results[0]
        assert result.scan_result_id == _TEST_SCAN_ID
        assert result.probe_lidar_id == "probe_1"
        assert result.probe_name == "Test Probe"
        assert result.probe_description == "A test probe"
        assert result.probe_tags == ["tag1", "tag2"]
        assert result.probe_category == "Category A"
        assert result.metrics == []
        assert result.progress.status == TaskStatus.FINISHED
        assert result.progress.total == 100
        assert result.progress.current == 100
        assert result.progress.error is None

    def test_scan_result_refresh(self, mock_client):
        scan = ScanResult.from_dict(
            {
                "id": _TEST_SCAN_ID,
                "project_id": _TEST_PROJECT_ID,
                "model": {"id": _TEST_MODEL_ID, "name": "Probe Model"},
                "start_datetime": "2023-10-01T12:00:00Z",
                "status": {
                    "state": "running",
                    "current": 0,
                    "total": 100,
                },
            },
            _client=mock_client,
        )

        assert scan.id == _TEST_SCAN_ID
        assert scan.progress.status == TaskStatus.RUNNING

        # Refresh
        scan.refresh()

        mock_client.scans.retrieve.assert_called_once()
        assert scan.id == _TEST_SCAN_ID
        assert scan.progress.status == TaskStatus.FINISHED
