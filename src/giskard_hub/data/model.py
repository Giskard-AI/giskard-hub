from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from ._base import BaseData
from ._entity import Entity
from .chat import ChatMessage


@dataclass
class ExecutionError(BaseData):
    """Model error."""

    message: str
    details: Dict[str, any] = field(default_factory=dict)


@dataclass
class ModelOutput(BaseData):
    """Model output."""

    message: ChatMessage | None = None
    metadata: Dict[str, any] = field(default_factory=dict)
    error: ExecutionError | None = None

    @classmethod
    def from_dict(cls, data: Dict[str, any], **kwargs) -> "BaseData":
        msg = data.get("response") or data.get("message")
        error = data.get("error")
        return cls(
            message=ChatMessage.from_dict(msg) if msg else None,
            metadata=data.get("metadata", {}),
            error=ExecutionError.from_dict(error) if error else None,
        )


@dataclass
class Model(Entity):
    """Model"""

    name: str
    project_id: str | None = None
    url: str | None = None
    description: str | None = None
    supported_languages: List[str] = field(default_factory=lambda: ["en"])
    headers: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, str], **kwargs) -> "Model":
        data = dict(data)
        headers = data.get("headers", {})
        if not isinstance(headers, dict):
            try:
                headers = {h["name"]: h["value"] for h in headers}
            except KeyError:
                raise ValueError("Invalid model headers.")

        data["headers"] = headers

        return super().from_dict(data, **kwargs)

    def chat(self, messages: List[ChatMessage]) -> ModelOutput:
        """Chat with the model.

        Parameters
        ----------
        messages : List[ChatMessage]
            A list of messages to send to the model.

        Returns
        -------
        ModelOutput
            The model response.
        """
        return self._client.models.chat(
            model_id=self.id,
            messages=messages,
        )
