from __future__ import annotations

import os
from typing import Callable, List, Optional

from ._base_client import SyncClient
from ._evaluation import LocalModel
from .data._base import NOT_GIVEN
from .data._entity import entity_to_id
from .data.chat import ChatMessage
from .data.dataset import Dataset
from .data.model import Model, ModelOutput
from .errors import HubConnectionError
from .resources.chat_test_cases import ChatTestCasesResource
from .resources.checks import ChecksResource
from .resources.conversations import ConversationsResource
from .resources.datasets import DatasetsResource
from .resources.evaluations import EvaluationsResource
from .resources.models import ModelsResource
from .resources.projects import ProjectsResource


# pylint: disable=too-many-instance-attributes
# The `conversations` resource is deprecated and will be removed in the future.
class HubClient(SyncClient):
    """Client class to handle interaction with the hub.

    Attributes
    ----------
    projects : ProjectsResource
        Resource to interact with projects.

    datasets : DatasetsResource
        Resource to interact with datasets.

    chat_test_cases : ChatTestCasesResource
        Resource to interact with chat test cases.

    conversations : ConversationsResource
        Resource to interact with conversations.

    models : ModelsResource
        Resource to interact with models.

    evaluations : EvaluationsResource
        Resource to interact with evaluations.

    evals : EvaluationsResource
        Alias for `evaluations`.
    """

    projects: ProjectsResource
    datasets: DatasetsResource
    chat_test_cases: ChatTestCasesResource
    conversations: ConversationsResource
    models: ModelsResource
    evaluations: EvaluationsResource
    checks: ChecksResource

    def __init__(
        self,
        hub_url: Optional[str] = None,
        api_key: Optional[str] = None,
        auto_add_api_suffix: Optional[bool] = True,
        **kwargs,
    ) -> None:
        """Initialize the client.

        Parameters
        ----------
        hub_url : str, optional
            URL of the Giskard Hub instance. If not provided, it will be read
            from the `GSK_HUB_URL` env variable.
        api_key : str, optional
            API key to authenticate with the Giskard Hub. If not provided, it
            will be read from the `GSK_API_KEY` env variable.
        auto_add_api_suffix : bool, optional
            If True, automatically adds the `_api` suffix to the `hub_url` if not already present.

        Raises
        ------
        ValueError
            If the `hub_url` or `api_key` are not provided and the environment
            variables are not set.
        HubConnectionError
            If calling `/openapi.json` fails or the response doesn't include an OpenAPI specification.
        """
        if hub_url is None:
            hub_url = os.getenv("GSK_HUB_URL")
        if hub_url is None:
            raise ValueError(
                "Missing Giskard Hub URL. Please provide it as an argument or set the env variable `GSK_HUB_URL`"
            )
        hub_url = hub_url.rstrip("/")
        if not hub_url.endswith("/_api") and auto_add_api_suffix:
            hub_url += "/_api"

        if api_key is None:
            api_key = os.getenv("GSK_API_KEY")

        if api_key is None:
            raise ValueError(
                "Missing Giskard Hub API key. Please provide it as an argument or with the env variable `GSK_API_KEY`"
            )

        self._hub_url = hub_url
        self._api_key = api_key

        super().__init__(**kwargs)

        # Set base url on the client
        self._http.base_url = self._hub_url

        # Check if the connection is valid
        try:
            resp = self._http.get("/openapi.json")
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            raise HubConnectionError(
                f"Failed to connect to Giskard Hub at {self._hub_url}"
            ) from e

        if "openapi" not in data:
            raise HubConnectionError(
                f"The response doesn't appear to include an OpenAPI specification at {self._hub_url}"
            )

        # Define the resources
        self.projects = ProjectsResource(self)
        self.datasets = DatasetsResource(self)
        self.chat_test_cases = ChatTestCasesResource(self)
        self.conversations = ConversationsResource(self)
        self.models = ModelsResource(self)
        self.evaluations = EvaluationsResource(self)
        self.checks = ChecksResource(self)

    @property
    def evals(self):
        return self.evaluations

    def _headers(self):
        return {
            "X-API-Key": self._api_key,
            "Content-Type": "application/json",
        }

    def evaluate(
        self,
        *,
        dataset: Dataset | str,
        tags: List[str] = NOT_GIVEN,
        model: Model | str | Callable[[List[ChatMessage]], ModelOutput | str],
        name: str = NOT_GIVEN,
    ):
        """Evaluate a model on a dataset.

        Parameters
        ----------
        dataset : str | Dataset
            ID of the dataset that will be used for the evaluation, or the dataset entity.
        tags: List[str], optional
            List of tags to filter the conversations (chat test cases) that will be evaluated.
        model : str | Model | Callable[[List[ChatMessage]], ModelOutput | str]
            ID of the model to evaluate, or a model entity, or a local model function.
            A local model function is a function that takes a list of messages and returns a `ModelOutput` or a string.
        name : str, optional
            The name of the evaluation run. If not provided, a random name will be automatically generated.

        Returns
        -------
        EvaluationRun
            The evaluation run entity.
        """
        is_local = False

        if isinstance(model, Callable):
            is_local = True
            model = LocalModel.from_callable(model)

        dataset_id = entity_to_id(dataset, Dataset)

        if is_local:
            return self._run_local_eval(
                dataset_id=dataset_id,
                tags=tags,
                model=model,
                name=name,
            )

        return self.evaluations.create(
            dataset_id=dataset_id,
            tags=tags,
            model_id=entity_to_id(model, Model),
            name=name,
        )

    def _run_local_eval(
        self, dataset_id: str, tags: List[str], model: LocalModel, name: str
    ):
        # Set up the evaluation run
        eval_run = self.evaluations.create_local(
            model=Model(name=model.name, description=model.description),
            dataset_id=dataset_id,
            tags=tags,
            name=name,
        )

        # Run the local model
        entries = self.evaluations.list_entries(eval_run.id)
        for entry in entries:
            model_output = model(entry.conversation.messages)
            self.evaluations.update_entry(
                eval_run.id, entry.id, model_output=model_output
            )

        return eval_run.refresh()
