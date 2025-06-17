from ..data.check import Check, extract_check_params
from ._resource import APIResource


class ChecksResource(APIResource):
    def list(self, project_id: str):
        data = self._client.get(f"/checks?project_id={project_id}&filter_builtin=true")

        return [
            Check.from_dict(
                {
                    **check,
                    "params": extract_check_params(check),
                }
            )
            for check in data
        ]

    def retrieve(self, check_id: str):
        data = self._client.get(f"/checks/{check_id}")
        return Check.from_dict(
            {
                **data,
                "params": extract_check_params(data),
            }
        )
