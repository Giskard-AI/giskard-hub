from __future__ import annotations

from typing import List

from ..data._base import NOT_GIVEN, filter_not_given
from ..data.scan import ScanResult
from ._resource import APIResource


class ScansResource(APIResource):
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
            "/scans",
            json=data,
            cast_to=ScanResult,
        )
