from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional


@dataclass
class BaseDataclass:
    """Base dataclass containing utility function."""

    @classmethod
    def from_dict(
        cls, data: Dict[str, Any], filter: Optional[List[str]] = None
    ) -> "Entity":
        """Class method factory, allowing to filter from a dict.

        Args:
            data (Dict[str, Any]): the data to use to initialise the dataclass
            filter (Optional[List[str]], optional): list of fields to ignore. Defaults to None.

        Returns:
        """
        if filter is None:
            filter = []
        return cls(**{k: v for k, v in data.items() if k not in filter})


@dataclass
class Entity(BaseDataclass):
    """Base class containing audit fields and id."""

    id: str
    created_at: datetime
    updated_at: datetime


@dataclass
class Project(Entity):
    """Project object (container with name and description)."""

    name: str
    description: str


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
class Dataset(Entity):
    """Dataset object, containing the metadata about the dataset."""

    project_id: str
    name: str
    description: str
    tags: List[str]


@dataclass
class Metric(BaseDataclass):
    """Metric object, with number of passed, failed and errored evaluations."""

    name: str
    passed: int
    failed: int
    errored: int
    total: int


@dataclass
class LLMMessage(BaseDataclass):
    """Message from an agent/llm, with role & content."""

    role: Literal["system", "assistant", "user"]
    content: str


@dataclass
class Conversation(Entity):
    """Dataset item, containing full conversation (ie messages), policies for compliance, expected_output for correctness and tags for filtering"""

    messages: List[LLMMessage]
    policies: List[str]
    tags: List[str]
    expected_output: Optional[str]
    demo_output: Optional[LLMMessage]

    @classmethod
    def from_dict(
        cls, data: Dict[str, Any], filter: Optional[List[str]] = None
    ) -> "Conversation":
        if filter is None:
            filter = ["dataset_id", "notes"]
        data: Conversation = super().from_dict(data, filter=filter)
        data.messages = (
            []
            if data.messages is None
            else [LLMMessage.from_dict(msg) for msg in data.messages]
        )
        data.demo_output = (
            None if data.demo_output is None else LLMMessage.from_dict(data.demo_output)
        )
        return data


@dataclass
class ModelOutput(BaseDataclass):
    """Expected format for an answer from an agent/model"""

    response: LLMMessage
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(
        cls, data: Dict[str, Any], filter: Optional[List[str]] = None
    ) -> "ModelOutput":
        data: ModelOutput = super().from_dict(data, filter=filter)
        data.response = LLMMessage.from_dict(data.response)
        return data


@dataclass
class Evaluation(Entity):
    """Single item evaluation, containing both the conversation, output of the agent and results of the evaluation."""

    execution_id: str
    conversation: Conversation
    output: Optional[ModelOutput] = field(default=None)
    error: Optional[str] = field(default=None)

    def set_output(self, output: str):
        """Convenience method to create a ModelOutput from a string.

        Args:
            output (str): the simple output from the model/agent
        """
        self.output = ModelOutput(response=LLMMessage(role="assistant", content=output))

    @classmethod
    def from_dict(
        cls, data: Dict[str, Any], filter: Optional[List[str]] = None
    ) -> "Evaluation":
        data: Evaluation = super().from_dict(data, filter=filter)
        data.conversation = Conversation.from_dict(data.conversation)
        data.output = (
            None if data.output is None else ModelOutput.from_dict(data.output)
        )
        return data


@dataclass
class TransientEvaluation(BaseDataclass):
    """Object to run a single evaluation without saving anything"""

    model_output: ModelOutput
    model_description: str
    messages: List[LLMMessage]
    policies: Optional[List[str]] = field(default_factory=list)
    expected_output: Optional[str] = field(default=None)

    @classmethod
    def from_dict(
        cls, data: Dict[str, Any], filter: Optional[List[str]] = None
    ) -> "TransientEvaluation":
        data: TransientEvaluation = super().from_dict(data, filter=filter)
        data.messages = (
            []
            if data.messages is None
            else [LLMMessage.from_dict(msg) for msg in data.messages]
        )
        data.model_output = (
            None
            if data.model_output is None
            else ModelOutput.from_dict(data.model_output)
        )
        return data


@dataclass
class TestResult(BaseDataclass):
    """Object containing the metric for a transient evaluation"""

    name: str
    passed: Optional[bool] = field(default=None)
    error: Optional[str] = field(default=None)
    reason: Optional[str] = field(default=None)
