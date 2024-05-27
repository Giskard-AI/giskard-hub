import json
import os
from dataclasses import asdict
from pathlib import Path
from time import sleep
from typing import List, Optional, Union

import requests

from giskard_hub.data import (
    Dataset,
    Evaluation,
    LLMMessage,
    Metric,
    Model,
    ModelOutput,
    Project,
    TestResult,
    TransientEvaluation,
)


class HubClient:
    """Client class to handle interaction with the hub."""

    # Note(Bazire): This is not async code, because it probably won't be used with async code.

    def __init__(
        self, hub_url: Optional[str] = None, api_key: Optional[str] = None
    ) -> None:
        if hub_url is None:
            hub_url = os.getenv("GSK_HUB_URL")
        if hub_url is None:
            raise ValueError(
                "Missing Giskard hub url. Please provide it as an argument or with the env variable `GSK_HUB_URL`"
            )

        if api_key is None:
            api_key = os.getenv("GSK_API_KEY")
        if api_key is None:
            raise ValueError(
                "Missing Giskard hub API key. Please provide it as an argument or with the env variable `GSK_API_KEY`"
            )
        self._hub_url = hub_url.rstrip("/")
        self._api_key = api_key

    def _headers(self):
        return {"X-API-Key": self._api_key}

    def _request(self, method: str, url: str, **kwargs):
        response = requests.request(
            **kwargs, method=method, url=url, headers=self._headers(), timeout=30
        )
        response.raise_for_status()
        return response.json()

    def evaluate(
        self,
        model_id: str,
        dataset_id: str,
        tags: Optional[List[str]] = None,
        local_mode: bool = True,
        use_file: bool = False,
        folder: Optional[Path] = None,
    ) -> Union[str, Path, List[Evaluation]]:
        """Start the evaluation of a model/agent on a dataset (or a subset).
        If local_mode is used, model output will need to be provided (else, hub will call model online).

        Args:
            model_id (str): the model to evaluate (still needed in local mode, since we are using agent description)
            dataset_id (str): the dataset to use for evaluation
            tags (list[str], optional): Tags to use to select a subset of the dataset. Defaults to None.
            local_mode (bool, optional): Whether agent output will be provided locally. Defaults to False.
            use_file (bool, optional): Whether to output evaluation dataset to file. Defaults to False.
            folder (Optional[Path], optional): Path to download the dataset to. Defaults to None (will be "evaluations/<execution_id>" if not provided).

        Returns:
            Union[str, Path, List[Evaluation]]]: In case of non local mode, execution object is returned.
            In case of local mode and use_file, the folder containing the dataset is provided
            In case of local mode and not use_file, a list of dict containing the evaluation data is provided.
        """

        dest = f"{self._hub_url}/executions/run"
        if local_mode:
            dest += "/async"
        # TODO(Bazire): use URL parse urllib
        print("Starting execution...")
        criteria = {"dataset_id": dataset_id}
        if tags is not None and len(tags) > 0:
            criteria["tags"] = tags
        data = self._request(
            "POST",
            dest,
            params={"model_id": model_id},
            json=[criteria],
        )

        execution_id: str = data["id"]

        if not local_mode:
            print("Execution started in the hub")
            # TODO(Bazire): provide link
            return execution_id

        print("Downloading dataset...")
        data = self._request(
            "GET",
            f"{self._hub_url}/executions/{execution_id}/results",
            params={"limit": 1000},
        )
        data = [
            Evaluation.from_dict(
                {
                    **elt,
                    "execution_id": execution_id,
                },
                filter=["results", "state"],
            )
            for elt in data["items"]
        ]
        if use_file:
            folder = Path("evaluations") / execution_id if folder is None else folder
            folder = folder.resolve()
            folder.mkdir(parents=True, exist_ok=True)
            for elt in data:
                file: Path = folder / (elt.id + ".json")
                file.write_text(json.dumps(asdict(elt)))
            print(f"Evaluation dataset saved locally at {str(folder)}")
            return folder
        return data

    def update_evaluations(
        self, evaluations: List[Evaluation]
    ) -> List[Optional[Evaluation]]:
        """Same as update_evaluation, but for a list of evaluations

        Args:
            evaluations (List[Evaluation]): list of the evaluation

        Returns:
            List[Optional[Evaluation]]: list of update data
        """
        return [self.update_evaluation(elt) for elt in evaluations]

    def update_evaluation(self, evaluation: Evaluation) -> Optional[Evaluation]:
        """Method to provide output to an evaluation

        Args:
            evaluation (Evaluation): dataclass containing the id of the evaluation, an output or an error key.

        Returns:
            Optional[Evaluation]: the update data, if not skipped
        """
        evaluation_id = evaluation.id
        output = evaluation.output
        error = evaluation.error

        if output is None and error is None:
            print(f"Skipping {evaluation_id} update since output and error are empty")
            return
        payload = {}
        if output is not None:
            if isinstance(output, str):
                output = ModelOutput(
                    response=LLMMessage(role="assistant", content=output)
                )
            if isinstance(output, ModelOutput):
                output = asdict(output)
            payload["output"] = output
        if error is not None:
            payload["error"] = error if isinstance(error, str) else str(error)
            # Note(Bazire): to improve/remove ?
        print(f"Updating {evaluation_id} ...")
        data = self._request(
            "PATCH", f"{self._hub_url}/executions/async/{evaluation_id}", json=payload
        )
        return Evaluation.from_dict(data, filter=["results", "state"])

    def get_results(
        self, execution_id: str, max_interval=20, interval_time=10
    ) -> List[Metric]:
        """Get the global results of the execution, waiting for it if it's still running

        Args:
            execution_id (str): if of the execution
            max_interval (int, optional): Number of try before stopping to get the results. Defaults to 20.
            interval_time (int, optional): Time in seconds to wait before retrying to get the results. Defaults to 10.

        Raises:
            ValueError: raised if the execution does not finish
            ValueError: raised if the execution ended up in error

        Returns:
            List[Metric]: the global metrics of the evaluation
        """
        nb_wait = 0
        done = False
        while not done and nb_wait < max_interval:
            data = self._request("GET", f"{self._hub_url}/executions/{execution_id}")
            state = data.get("status", {}).get("state", "unknown")

            if state == "running":
                current = data.get("status", {}).get("current")
                total = data.get("status", {}).get("total")
                print(
                    f"Evaluation not finished ({current}/{total}), waiting for {interval_time}s"
                )
                sleep(interval_time)
            else:
                done = True

        if nb_wait > max_interval:
            raise ValueError(
                "Evaluation did not finished running in the allotted time, did you provide all outputs ?"
            )
        if state != "finished":
            raise ValueError(
                "Evaluation ended in error, please visit the hub for more details"
            )
        return [Metric(**elt) for elt in data.get("metrics", [])]

    def get_projects(self) -> list[Project]:
        """List the projects in the hub.

        Returns:
            list[Project]: list of the projects
        """
        return [
            Project.from_dict(elt)
            for elt in self._request("GET", f"{self._hub_url}/projects")
        ]

    def get_datasets(self, project_id: str) -> list[Dataset]:
        """List the datasets into the target project.

        Args:
            project_id (str): id of the project

        Returns:
            list[Dataset]: the list of datasets
        """
        return [
            Dataset.from_dict(elt, filter=["status"])
            for elt in self._request(
                "GET", f"{self._hub_url}/datasets", params={"project_id": project_id}
            )
        ]

    def get_models(self, project_id: str) -> list[Model]:
        """List the models into the target project.

        Args:
            project_id (str): id of the project

        Returns:
            list[Model]: the list of models
        """
        return [
            Model.from_dict(elt)
            for elt in self._request(
                "GET", f"{self._hub_url}/models", params={"project_id": project_id}
            )
        ]

    def single_eval(self, to_eval: TransientEvaluation) -> list[TestResult]:
        """Run the transient evaluation on a single conversation.

        Args:
            to_eval (TransientEvaluation): the

        Returns:
            list[TestResult]: List of test results, with reason & error if any.
        """
        return [
            TestResult.from_dict(elt, filter=["status"])
            for elt in self._request(
                "POST", f"{self._hub_url}/executions/single", json=asdict(to_eval)
            )
        ]
