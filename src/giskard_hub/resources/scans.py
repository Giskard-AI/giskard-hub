from typing import List

from ..data._base import NOT_GIVEN, filter_not_given
from ..data.scan import (
    SCAN_CATEGORIES,
    ProbeAttempt,
    ProbeResult,
    ScanCategory,
    ScanResult,
)
from ._resource import APIResource

_SCAN_BASE_URL = "/scans"
_PROBE_BASE_URL = "/probes"


class ScansResource(APIResource):
    def list_tags(self) -> List[ScanCategory]:
        """List scan categories that can be use as tags.

        Returns:
            List[ScanCategory]: A list of `ScanCategory` objects representing all available scan categories.
        """
        return SCAN_CATEGORIES

    def create(
        self,
        *,
        model_id: str,
        knowledge_base_id: str = NOT_GIVEN,
        tags: List[str] = NOT_GIVEN,
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

    def retrieve_probe(self, probe_result_id: str) -> ProbeResult:
        """Get a probe result by its ID.

        Parameters
        ----------
        probe_result_id : str
            The ID of the probe result to retrieve.

        Returns
        -------
        ProbeResult
            The retrieved probe result.
        """
        return self._client.get(
            f"{_PROBE_BASE_URL}/{probe_result_id}", cast_to=ProbeResult
        )

    def get_attempts(self, probe_result_id: str) -> List[ProbeAttempt]:
        """Get all probe attempts for a given probe result.

        Parameters
        ----------
        probe_result_id : str
            The ID of the probe result to get attempts for.

        Returns
        -------
        List[ProbeAttempt]
            List of probe attempts for the given probe result.
        """
        return [
            ProbeAttempt.from_dict(r)
            for r in self._client.get(f"{_PROBE_BASE_URL}/{probe_result_id}/attempts")[
                "items"
            ]
        ]
