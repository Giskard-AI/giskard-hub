from typing import List

from giskard_hub.data.scan import ProbeResult, ScanResult
from giskard_hub.resources._resource import APIResource

_SCAN_BASE_URL = "/scans"


class ScansResource(APIResource):
    def retrieve(self, scan_id: str) -> ScanResult:
        return self._client.get(f"{_SCAN_BASE_URL}/{scan_id}", cast_to=ScanResult)

    def list(self, project_id: str) -> List[ScanResult]:
        return self._client.get(
            _SCAN_BASE_URL,
            cast_to=ScanResult,
            json={"project_id": project_id},
        )

    def delete(self, scan_id: str) -> None:
        # Delete a scan by its ID in a list
        self._client.delete(_SCAN_BASE_URL, json=[scan_id])

    def get_probes(self, scan_id: str) -> List[ProbeResult]:
        return self._client.get(
            f"{_SCAN_BASE_URL}/{scan_id}/probes",
            cast_to=List[ProbeResult],
        )
