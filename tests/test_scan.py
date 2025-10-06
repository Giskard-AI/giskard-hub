


import uuid
from giskard_hub.data.task import TaskStatus

from giskard_hub.data.scan import ScanResult


class TestScanResultDataModel:
    """Test the Scan data model."""

    def test_scan_result_from_dict_basic(self):
        project_id = str(uuid.uuid4())
        scan_dict = {
            "id": "scan_123",
            "project_id": project_id,
            "model": {"id": "model_789", "name": "Test Model"},
            "status": {
                "state": "finished",
                "total": 100,
                "current": 100,
            },
            "grade": "A",
        }

        scan = ScanResult.from_dict(scan_dict)

        assert scan.id == "scan_123"
        assert scan.project_id == project_id
        assert scan.model.id == "model_789"
        assert scan.model.name == "Test Model"
        assert scan.progress.status == TaskStatus.FINISHED
        assert scan.progress.total == 100
        assert scan.progress.current == 100
        assert scan.grade == "A"

    def test_scan_result_from_dict_minimal(self):
        project_id = str(uuid.uuid4())
        scan_dict = {
            "id": "scan_001",
            "project_id": project_id,
            "model": {"id": "model_001", "name": "Minimal Model"},
        }

        scan = ScanResult.from_dict(scan_dict)

        assert scan.id == "scan_001"
        assert scan.model.id == "model_001"
        assert scan.model.name == "Minimal Model"
        assert scan.project_id == project_id
        assert scan.progress is None
        assert scan.grade is None

    
