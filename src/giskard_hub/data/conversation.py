from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ._base import BaseData
from ._entity import Entity
from .chat import ChatMessage


@dataclass
class CheckConfiguration(BaseData):
    check: str
    params: dict[str, Any]


@dataclass
class Conversation(Entity):
    """A Dataset entry representing a conversation.

    Attributes
    ----------
    messages : List[ChatMessage]
        List of messages in the conversation. Each message is an object with a role and content attributes.
    demo_output : Optional[ChatMessage], optional
        Output of the agent for demonstration purposes.
    tags : List[str], optional
        List of tags for the conversation.
    checks : List[CheckConfiguration], optional
        List of checks to be performed on the conversation.
    """

    messages: List[ChatMessage] = field(default_factory=list)
    demo_output: Optional[ChatMessage] = field(default=None)
    tags: List[str] = field(default_factory=list)
    checks: List[CheckConfiguration] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> "Conversation":
        obj = super().from_dict(data, **kwargs)
        obj.messages = (
            []
            if obj.messages is None
            else [ChatMessage.from_dict(msg) for msg in obj.messages]
        )
        obj.demo_output = (
            None if obj.demo_output is None else ChatMessage.from_dict(obj.demo_output)
        )
        return obj
