from giskard_hub.data.scan import ProbeResult
from giskard_hub.resources._resource import APIResource

_PROBE_BASE_URL = "/probes"


class ProbesResource(APIResource):
    def retrieve(self, probe_result_id: str) -> ProbeResult:
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
        return self.client.get(f"{_PROBE_BASE_URL}/{probe_result_id}", cast_to=ProbeResult)

    def get_attempts(self, probe_result_id: str):
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
            ProbeResult.from_dict(r)
            for r in self.client.get(f"{_PROBE_BASE_URL}/{probe_result_id}/attempts")[
                "items"
            ]
        ]
