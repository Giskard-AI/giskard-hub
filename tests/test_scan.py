import uuid
from unittest.mock import MagicMock

import pytest

from giskard_hub.data.scan import ProbeResult, ScanGrade, ScanResult, ScanType
from giskard_hub.data.task import TaskStatus
from giskard_hub.resources.scans import ScansResource

_TEST_PROBE_ID = str(uuid.uuid4())
_TEST_SCAN_ID = str(uuid.uuid4())
_TEST_PROJECT_ID = str(uuid.uuid4())
_TEST_MODEL_ID = str(uuid.uuid4())


_test_scan = {
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

_test_running_scan = {
    "id": _TEST_SCAN_ID,
    "project_id": _TEST_PROJECT_ID,
    "model": {"id": _TEST_MODEL_ID, "name": "Probe Model"},
    "start_datetime": "2023-10-01T12:00:00Z",
    "status": {
        "state": "running",
        "current": 0,
        "total": 100,
    },
}

_test_probe = {
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


@pytest.fixture
def mock_client():
    """Mock client for testing."""
    mock_client = MagicMock()

    # GET /scans/{scan_id}/probes to get probe results for a scan
    mock_client.scans.get_probes.return_value = [
        ProbeResult.from_dict(r, _client=mock_client)
        for r in [
            _test_probe,
        ]
    ]

    # GET /scans/{scan_id} to retrieve a specific scan
    mock_client.scans.retrieve.return_value = ScanResult.from_dict(
        _test_scan, _client=mock_client
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
        """Test initilizing with minimum fields"""
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
        """Test initilizing with probe errors"""
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
        """Test getting probe results of a scan"""
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
        """Test scan result refresh"""
        scan = ScanResult.from_dict(
            _test_running_scan,
            _client=mock_client,
        )

        assert scan.id == _TEST_SCAN_ID
        assert scan.progress.status == TaskStatus.RUNNING

        # Refresh
        scan.refresh()

        mock_client.scans.retrieve.assert_called_once()
        assert scan.id == _TEST_SCAN_ID
        assert scan.progress.status == TaskStatus.FINISHED

    def test_scan_result_block_waiting(self, mock_client):
        """Test waiting for task completion"""
        scan = ScanResult.from_dict(
            _test_running_scan,
            _client=mock_client,
        )

        assert scan.id == _TEST_SCAN_ID
        assert scan.progress.status == TaskStatus.RUNNING

        scan.wait_for_completion()

        # Equal to scan.refresh() so that this method is called
        mock_client.scans.retrieve.assert_called_once()
        assert scan.id == _TEST_SCAN_ID
        assert scan.progress.status == TaskStatus.FINISHED


@pytest.fixture
def mock_http_client():
    """Mock HTTP client for testing API resources."""
    mock_client = MagicMock()

    def handle_get_response(path, cast_to=None, **kwargs):
        response_data = mock_client.get.return_value
        if cast_to is None:
            return response_data

        if cast_to == ScanResult:
            return ScanResult.from_dict(response_data)
        elif cast_to == ProbeResult:
            return ProbeResult.from_dict(response_data)

        return response_data

    # GET
    mock_client.get.side_effect = handle_get_response

    # POST
    mock_client.post.side_effect = lambda path, cast_to=None, **kwargs: (
        ScanResult.from_dict(mock_client.post.return_value)
        if cast_to == ScanResult
        else mock_client.post.return_value
    )

    # PATCH
    mock_client.patch.side_effect = lambda path, cast_to=None, **kwargs: (
        ScanResult.from_dict(mock_client.patch.return_value)
        if cast_to == ScanResult
        else mock_client.patch.return_value
    )

    # DELETE
    mock_client.delete.side_effect = lambda path, **kwargs: None

    return mock_client


class TestScanResultResource:
    """Test the Scan API resources."""

    def test_scan_resource_list(self, mock_http_client):
        """Test listing all scan results for a project"""
        mock_http_client.get.return_value = {
            "items": [
                _test_scan,
            ],
        }

        resource = ScansResource(mock_http_client)

        scans = resource.list(_TEST_PROJECT_ID)
        assert len(scans) == 1

        scan = scans[0]
        assert scan.id == _TEST_SCAN_ID
        assert scan.project_id == _TEST_PROJECT_ID
        assert scan.progress.status == TaskStatus.FINISHED

        mock_http_client.get.assert_called_once()

    def test_scan_resource_retrieve(self, mock_http_client):
        """Test retrieving a scan result with a given scan id"""
        mock_http_client.get.return_value = _test_scan

        resource = ScansResource(mock_http_client)
        scan = resource.retrieve(_TEST_SCAN_ID)

        assert scan is not None
        assert scan.id == _TEST_SCAN_ID
        assert scan.project_id == _TEST_PROJECT_ID
        assert scan.progress.status == TaskStatus.FINISHED

        mock_http_client.get.assert_called_once()

    def test_scan_resource_create(self, mock_http_client):
        """Test creating a scan"""
        mock_http_client.post.return_value = _test_running_scan

        resource = ScansResource(mock_http_client)
        scan = resource.create(model_id=_TEST_MODEL_ID)

        assert scan is not None
        assert scan.id == _TEST_SCAN_ID
        assert scan.project_id == _TEST_PROJECT_ID
        assert scan.progress.status == TaskStatus.RUNNING

        mock_http_client.post.assert_called_once()

    def test_scan_resource_delete(self, mock_http_client):
        """Test deleting a scan result"""
        resource = ScansResource(mock_http_client)
        resource.delete(_TEST_SCAN_ID)

        mock_http_client.delete.assert_called_once()

    def test_scan_resource_get_probes(self, mock_http_client):
        """Test getting probe results from a scan result"""
        mock_http_client.get.return_value = {
            "items": [
                _test_probe,
            ],
        }

        resource = ScansResource(mock_http_client)
        probes = resource.get_probes(_TEST_SCAN_ID)

        assert len(probes) == 1

        probe = probes[0]
        assert probe.id == _TEST_PROBE_ID
        assert probe.scan_result_id == _TEST_SCAN_ID
