from typing import List, Optional

from ..data._base import NOT_GIVEN, filter_not_given
from ..data.scan import (
    ProbeAttempt,
    ProbeResult,
    ScanCategory,
    ScanResult,
)
from ._resource import APIResource

_SCAN_BASE_URL = "/scans"
_PROBE_BASE_URL = "/probes"


class ScansResource(APIResource):
    def list_categories(self) -> List[ScanCategory]:
        """List scan categories that can be use as tags to create/launch a scan.

        Returns
        -------
            List[ScanCategory]: A list of `ScanCategory` objects representing all available scan categories.
        """
        data = self._client.get(f"{_SCAN_BASE_URL}/categories")
        return [ScanCategory.from_dict(item) for item in data["items"]]

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
            List of tags to limit the scan to specific categories. If not provided, all categories will be used.

        Returns
        -------
        ScanResult
            The created scan result.
        """
        if not tags or len(tags) == 0:
            tags = [category.id for category in self.list_categories()]

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

    def list(self, project_id: Optional[str] = None) -> List[ScanResult]:
        """List all scans or optionally for a given project.

        Parameters
        ----------
        project_id : str, optional
            ID of the project to list scans for. If not provided, scans for all projects will be listed.

        Returns
        -------
        List[ScanResult]
            List of scan results.
        """
        return [
            ScanResult.from_dict(r, _client=self._client)
            for r in self._client.get(
                (
                    _SCAN_BASE_URL
                    if project_id is None
                    else f"{_SCAN_BASE_URL}?project_id={project_id}"
                ),
            )["items"]
        ]

    def delete(self, scan_id: str | List[str]) -> None:
        """Delete a scan by its ID.

        Parameters
        ----------
        scan_id : str | List[str]
            ID or list of IDs of the scan to delete.

        Returns
        -------
        None
            None
        """
        self._client.delete(_SCAN_BASE_URL, params={"scan_result_ids": scan_id})

    def retrieve_probe(self, probe_result_id: str) -> ProbeResult:
        """Retrieve a probe result by its ID.

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

    def list_probes(self, scan_id: str) -> List[ProbeResult]:
        """List all probe results for a given scan.

        Parameters
        ----------
        scan_id : str
            ID of the scan to list probes for.

        Returns
        -------
        List[ProbeResult]
            List of probe results for the given scan.
        """
        return [
            ProbeResult.from_dict(r, _client=self._client)
            for r in self._client.get(
                f"{_SCAN_BASE_URL}/{scan_id}/probes",
            )["items"]
        ]

    def list_attempts(self, probe_result_id: str) -> List[ProbeAttempt]:
        """List all attempts (attacks) for a given probe result.

        Parameters
        ----------
        probe_result_id : str
            The ID of the probe result to list attempts for.

        Returns
        -------
        List[ProbeAttempt]
            List of attempts for the given probe result.
        """
        return [
            ProbeAttempt.from_dict(r, _client=self._client)
            for r in self._client.get(f"{_PROBE_BASE_URL}/{probe_result_id}/attempts")[
                "items"
            ]
        ]
