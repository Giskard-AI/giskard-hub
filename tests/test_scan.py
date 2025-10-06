import uuid

from giskard_hub.data.scan import ScanResult, ScanType
from giskard_hub.data.task import TaskStatus


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
            "grade": "A",
            "lidar_version": "1.0.0",
            "tags": ["tag1", "tag2"],
            "scan_type": ScanType.DEFAULT.value,
            "errors": [],
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
        assert scan.scan_type == ScanType.DEFAULT
        assert scan.errors == []

    def test_scan_result_from_dict_minimal(self):
        scan_id = str(uuid.uuid4())
        project_id = str(uuid.uuid4())
        model_id = str(uuid.uuid4())
        scan_dict = {
            "id": scan_id,
            "project_id": project_id,
            "model": {"id": model_id, "name": "Minimal Model"},
            "errors": [],
            "scan_type": ScanType.DEFAULT.value,
        }

        scan = ScanResult.from_dict(scan_dict)

        assert scan.id == scan_id
        assert scan.model.id == model_id
        assert scan.model.name == "Minimal Model"
        assert scan.project_id == project_id
        assert scan.progress is None
        assert scan.grade is None

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
            "scan_type": ScanType.DEFAULT.value,
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
