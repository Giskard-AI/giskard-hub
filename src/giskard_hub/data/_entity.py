from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from typing_extensions import Any, Dict, List

if TYPE_CHECKING:
    from ..client import HubClient

from ._base import BaseData


def maybe_entity_to_id(entity, EntityClass=None):
    if entity is None:
        return None

    return entity_to_id(entity, EntityClass)


def entity_to_id(entity, EntityClass=None):
    if isinstance(entity, str):
        return entity

    if EntityClass is None:
        return entity.id

    if isinstance(entity, EntityClass):
        return entity.id

    raise ValueError(
        f"Invalid {EntityClass.__name__} provided, got object of type {type(entity)}"
    )


@dataclass
class Entity(BaseData):
    """Base class containing audit fields and id."""

    id: str | None = field(init=False, default=None)
    created_at: datetime | None = field(init=False, default=None)
    updated_at: datetime | None = field(init=False, default=None)

    _client: Optional["HubClient"] = field(init=False, repr=False, default=None)

    @classmethod
    def from_dict(
        cls, data: Dict[str, Any], *, _client: Optional["HubClient"] = None
    ) -> "Entity":
        """Class method factory, allowing to filter from a dict.

        Parameters
        ----------
        data : Dict[str, Any]
            The data to use to initialize the dataclass.
        """
        data = dict(data)

        raw_created_at = data.get("created_at", None)
        raw_updated_at = data.get("updated_at", None)

        if raw_created_at:
            data["created_at"] = datetime.fromisoformat(raw_created_at)

        if raw_updated_at:
            data["updated_at"] = datetime.fromisoformat(raw_updated_at)

        entity = super().from_dict(data)
        entity._client = _client
        return entity

    def _hydrate(self, data: "Entity"):
        """Hydrate with the data from the API."""
        # @TODO: make this more robust
        for key, value in data.__dict__.items():
            setattr(self, key, value)


@dataclass
class Model(Entity):
    """Model/agent object, containing miscelleanous info about the model?"""

    project_id: str
    name: str
    url: str
    description: str
    supported_languages: List[str]
    headers: List[Dict[str, str]]


@dataclass
class Metric(BaseData):
    """Metric object, with number of passed, failed and errored evaluations."""

    name: str
    passed: int
    failed: int
    errored: int
    total: int


# @dataclass
# class Conversation(Entity):
#     """A Dataset entry representing a conversation.

#     Attributes
#     ----------
#     messages : List[LLMMessage]
#         List of messages in the conversation. Each message is an object with a role and content attributes.
#     tags : List[str], optional
#         List of tags for the conversation.
#     expected_output : Optional[str], optional
#         Expected output which will be used for correctness evaluation.
#     policies : List[str], optional
#         List of policies used for evaluation.
#     demo_output : Optional[LLMMessage], optional
#         Output of the agent for demonstration purposes.
#     """

#     messages: List[ChatMessage]
#     policies: List[str]
#     tags: List[str]
#     expected_output: Optional[str]
#     demo_output: Optional[ChatMessage]

#     @classmethod
#     def from_dict(
#         cls, data: Dict[str, Any], filter: Optional[List[str]] = None
#     ) -> "Conversation":
#         if filter is None:
#             filter = ["dataset_id", "notes"]
#         data: Conversation = super().from_dict(data, filter=filter)
#         data.messages = (
#             []
#             if data.messages is None
#             else [ChatMessage.from_dict(msg) for msg in data.messages]
#         )
#         data.demo_output = (
#             None
#             if data.demo_output is None
#             else ChatMessage.from_dict(data.demo_output)
#         )
#         return data


# @dataclass
# class ModelOutput(BaseDataclass):
#     """Expected format for an answer from an agent/model"""

#     response: ChatMessage
#     metadata: dict[str, Any] = field(default_factory=dict)

#     @classmethod
#     def from_dict(
#         cls, data: Dict[str, Any], filter: Optional[List[str]] = None
#     ) -> "ModelOutput":
#         data: ModelOutput = super().from_dict(data, filter=filter)
#         data.response = ChatMessage.from_dict(data.response)
#         return data


# @dataclass
# class Evaluation(Entity):
#     """Single item evaluation, containing both the conversation, output of the agent and results of the evaluation."""

#     execution_id: str
#     conversation: Conversation
#     output: Optional[ModelOutput] = field(default=None)
#     error: Optional[str] = field(default=None)

#     def set_output(self, output: str):
#         """Convenience method to create a ModelOutput from a string.

#         Args:
#             output (str): the simple output from the model/agent
#         """
#         self.output = ModelOutput(
#             response=ChatMessage(role="assistant", content=output)
#         )

#     @classmethod
#     def from_dict(
#         cls, data: Dict[str, Any], filter: Optional[List[str]] = None
#     ) -> "Evaluation":
#         data: Evaluation = super().from_dict(data, filter=filter)
#         data.conversation = Conversation.from_dict(data.conversation)
#         data.output = (
#             None if data.output is None else ModelOutput.from_dict(data.output)
#         )
#         return data


# @dataclass
# class TransientEvaluation(BaseDataclass):
#     """Object to run a single evaluation without saving anything"""

#     model_output: ModelOutput
#     model_description: str
#     messages: List[ChatMessage]
#     policies: Optional[List[str]] = field(default_factory=list)
#     expected_output: Optional[str] = field(default=None)

#     @classmethod
#     def from_dict(
#         cls, data: Dict[str, Any], filter: Optional[List[str]] = None
#     ) -> "TransientEvaluation":
#         data: TransientEvaluation = super().from_dict(data, filter=filter)
#         data.messages = (
#             []
#             if data.messages is None
#             else [ChatMessage.from_dict(msg) for msg in data.messages]
#         )
#         data.model_output = (
#             None
#             if data.model_output is None
#             else ModelOutput.from_dict(data.model_output)
#         )
#         return data


# @dataclass
# class TestResult(BaseDataclass):
#     """Object containing the metric for a transient evaluation"""

#     name: str
#     passed: Optional[bool] = field(default=None)
#     error: Optional[str] = field(default=None)
#     reason: Optional[str] = field(default=None)
