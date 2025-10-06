import uuid

import pytest

from giskard_hub.data.scan import ScanResult, ScanType
from giskard_hub.data.task import TaskStatus

_TEST_SCAN_ID = str(uuid.uuid4())


@pytest.fixture
def mock_client():
    """Mock client for testing."""

    class MockClient:
        def get(self, url):
            if url.endswith("/probes"):
                return {
                    "items": [
                        {
                            "id": str(uuid.uuid4()),
                            "scan_result_id": _TEST_SCAN_ID,
                            "probe_lidar_id": "probe_1",
                            "probe_name": "Test Probe",
                            "probe_description": "A test probe",
                            "probe_tags": ["tag1", "tag2"],
                            "probe_category": "Category A",
                            "metrics": [],
                            "status": {
                                "state": "finished",
                                "current": 100,
                                "total": 100,
                                "error": None,
                            },
                        },
                    ],
                }

    return MockClient()


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
            "grade": "A",
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
        assert scan.grade == "A"
        assert scan.lidar_version == "1.0.0"
        assert scan.tags == ["tag1", "tag2"]
        assert scan.scan_type == ScanType.IN_DEPTH
        assert scan.errors == []
        assert scan.generator_metadata == {}
        assert scan.target_info == {}
        assert scan.scan_metadata == {}

    def test_scan_result_from_dict_minimal(self):
        project_id = str(uuid.uuid4())
        model_id = str(uuid.uuid4())
        scan_dict = {
            "id": _TEST_SCAN_ID,
            "project_id": project_id,
            "model": {"id": model_id, "name": "Minimal Model"},
        }

        scan = ScanResult.from_dict(scan_dict)

        assert scan.id == _TEST_SCAN_ID
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
        project_id = str(uuid.uuid4())
        model_id = str(uuid.uuid4())
        scan_dict = {
            "id": _TEST_SCAN_ID,
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

        assert scan.id == _TEST_SCAN_ID
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

    def test_scan_result_probes_property(self, mock_client):
        project_id = str(uuid.uuid4())
        model_id = str(uuid.uuid4())
        scan_dict = {
            "id": _TEST_SCAN_ID,
            "project_id": project_id,
            "model": {"id": model_id, "name": "Probe Model"},
        }

        scan = ScanResult.from_dict(scan_dict)
        scan._client = mock_client

        probes = scan.probes
        assert len(probes) == 1
        probe = probes[0]
        assert probe.scan_result_id == _TEST_SCAN_ID
        assert probe.probe_lidar_id == "probe_1"
        assert probe.probe_name == "Test Probe"
        assert probe.probe_description == "A test probe"
        assert probe.probe_tags == ["tag1", "tag2"]
        assert probe.probe_category == "Category A"
        assert probe.metrics == []
        assert probe.progress.status == TaskStatus.FINISHED
        assert probe.progress.total == 100
        assert probe.progress.current == 100
        assert probe.progress.error is None
