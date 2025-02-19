from __future__ import annotations

from typing import List

from ..data._base import NOT_GIVEN, filter_not_given, maybe_to_dict
from ..data.evaluation import EvaluationEntry, EvaluationRun, EvaluatorResult
from ..data.model import Model, ModelOutput
from ._resource import APIResource


class EvaluationsResource(APIResource):
    def retrieve(self, run_id: str):
        return self._client.get(f"/executions/{run_id}", cast_to=EvaluationRun)

    def create(
        self,
        *,
        model_id: str,
        dataset_id: str,
        tags: List[str] = NOT_GIVEN,
        name: str = NOT_GIVEN,
    ):
        data = filter_not_given(
            {
                "name": name,
                "model_id": model_id,
            }
        )
        data["criteria"] = [
            filter_not_given(
                {
                    "dataset_id": dataset_id,
                    "tags": tags,
                }
            )
        ]

        return self._client.post(
            "/executions",
            json=data,
            cast_to=EvaluationRun,
        )

    def create_local(
        self,
        *,
        model: Model,
        dataset_id: str,
        tags: List[str] = NOT_GIVEN,
        name: str = NOT_GIVEN,
    ):
        data = filter_not_given(
            {
                "name": name,
                "model": model.to_dict(),
            }
        )
        data["criteria"] = [
            filter_not_given(
                {
                    "dataset_id": dataset_id,
                    "tags": tags,
                }
            )
        ]

        return self._client.post(
            "/executions/local",
            json=data,
            cast_to=EvaluationRun,
        )

    def delete(self, execution_id: str | List[str]):
        return self._client.delete(
            "/executions", params={"execution_ids": execution_id}
        )

    def list(self, project_id: str):
        return self._client.get(
            "/executions", params={"project_id": project_id}, cast_to=EvaluationRun
        )

    def list_entries(self, run_id: str):
        entries = self._client.get(f"/executions/{run_id}/results?limit=100_000")[
            "items"
        ]
        return [EvaluationEntry.from_dict(entry) for entry in entries]

    def update_entry(
        self,
        run_id: str,
        entry_id: str,
        *,
        model_output: ModelOutput = NOT_GIVEN,
        results: List[EvaluatorResult] = NOT_GIVEN,
    ):
        if model_output and not isinstance(model_output, ModelOutput):
            model_output = ModelOutput.from_dict(model_output)

        if model_output:
            output = {
                "response": model_output.message.to_dict(),
                "metadata": model_output.metadata,
            }
        else:
            output = NOT_GIVEN

        data = filter_not_given(
            {
                "output": output,
                "results": (
                    [maybe_to_dict(result) for result in results]
                    if results
                    else NOT_GIVEN
                ),
            }
        )
        return self._client.patch(
            f"/executions/{run_id}/results/{entry_id}",
            json=data,
            cast_to=EvaluationEntry,
        )
