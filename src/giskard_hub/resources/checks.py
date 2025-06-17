from ..data.check import Check, extract_check_params
from ._resource import APIResource


class ChecksResource(APIResource):
    def list(self, project_id: str):
        data = self._client.get(f"/checks?project_id={project_id}&filter_builtin=true")

        checks = [
            Check.from_dict(
                {
                    **check,
                    "params": extract_check_params(check),
                }
            )
            for check in data
        ]

        return checks
