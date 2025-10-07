from typing import List

from ..data._base import NOT_GIVEN, filter_not_given
from ..data.scan import ProbeResult, ScanResult, ScanType
from ._resource import APIResource

_SCAN_BASE_URL = "/scans"


class ScansResource(APIResource):
    def create(
        self,
        *,
        model_id: str,
        knowledge_base_id: str = NOT_GIVEN,
        tags: List[str] = NOT_GIVEN,
        scan_type: ScanType = NOT_GIVEN,
    ) -> ScanResult:
        """Create and run a new scan.

        Parameters
        ----------
        model_id : str
            ID of the model to scan.
        knowledge_base_id : str, optional
            ID of the knowledge base to use for the scan.
        tags : List[str], optional
            List of tags to filter the scan.
        scan_type : ScanType, optional
            Type of the scan to run.

        Returns
        -------
        ScanResult
            The created scan result.
        """
        data = filter_not_given(
            {
                "model_id": model_id,
                "knowledge_base_id": knowledge_base_id,
                "tags": tags,
                "scan_type": scan_type,
            }
        )

        return self._client.post(
            _SCAN_BASE_URL,
            json=data,
            cast_to=ScanResult,
        )

    def retrieve(self, scan_id: str) -> ScanResult:
        """Retrieve a scan by its ID.
        Parameters
        ----------
        scan_id : str
            ID of the scan to retrieve.
        Returns
        -------
        ScanResult
            The retrieved scan result.
        """
        return self._client.get(f"{_SCAN_BASE_URL}/{scan_id}", cast_to=ScanResult)

    def list(self, project_id: str) -> List[ScanResult]:
        """List all scans for a given project.
        Parameters
        ----------
        project_id : str
            ID of the project to list scans for.
        Returns
        -------
        List[ScanResult]
            List of scan results for the given project.
        """
        return [
            ScanResult.from_dict(r)
            for r in self._client.get(
                _SCAN_BASE_URL,
                cast_to=ScanResult,
                json={"project_id": project_id},
            )["items"]
        ]

    def delete(self, scan_id: str) -> None:
        """Delete a scan by its ID.

        Parameters
        ----------
        scan_id : str
            ID of the scan to delete.
        Returns
        -------
        None
            None
        """
        # Delete a scan by its ID in a list
        self._client.delete(_SCAN_BASE_URL, json=[scan_id])

    def get_probes(self, scan_id: str) -> List[ProbeResult]:
        """Get all probe results for a given scan.

        Parameters
        ----------
        scan_id : str
            ID of the scan to get probes for.
        Returns
        -------
        List[ProbeResult]
            List of probe results for the given scan.
        """
        return [
            ProbeResult.from_dict(r)
            for r in self._client.get(
                f"{_SCAN_BASE_URL}/{scan_id}/probes",
            )["items"]
        ]
