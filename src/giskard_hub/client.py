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
from .resources.conversations import ConversationsResource
from .resources.datasets import DatasetsResource
from .resources.evaluations import EvaluationsResource
from .resources.models import ModelsResource
from .resources.projects import ProjectsResource


class HubClient(SyncClient):
    """Client class to handle interaction with the hub.

    Attributes
    ----------
    projects : ProjectsResource
        Resource to interact with projects.

    datasets : DatasetsResource
        Resource to interact with datasets.

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
    conversations: ConversationsResource
    models: ModelsResource
    evaluations: EvaluationsResource

    def __init__(
        self,
        hub_url: Optional[str] = None,
        api_key: Optional[str] = None,
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

        Raises
        ------
        ValueError
            If the `hub_url` or `api_key` are not provided and the environment
            variables are not set.
        """
        if hub_url is None:
            hub_url = os.getenv("GSK_HUB_URL")
        if hub_url is None:
            raise ValueError(
                "Missing Giskard Hub URL. Please provide it as an argument or set the env variable `GSK_HUB_URL`"
            )

        if api_key is None:
            api_key = os.getenv("GSK_API_KEY")
        if api_key is None:
            raise ValueError(
                "Missing Giskard Hub API key. Please provide it as an argument or with the env variable `GSK_API_KEY`"
            )
        self._hub_url = hub_url.rstrip("/")
        self._api_key = api_key

        super().__init__(**kwargs)

        # Set base url on the client
        self._http.base_url = self._hub_url

        # Define the resources
        self.projects = ProjectsResource(self)
        self.datasets = DatasetsResource(self)
        self.conversations = ConversationsResource(self)
        self.models = ModelsResource(self)
        self.evaluations = EvaluationsResource(self)

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
            List of tags to filter the conversations that will be evaluated.
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
