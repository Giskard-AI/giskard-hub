from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ._entity import Entity
from .chat import ChatMessage


@dataclass
class Conversation(Entity):
    """A Dataset entry representing a conversation.

    Attributes
    ----------
    messages : List[ChatMessage]
        List of messages in the conversation. Each message is an object with a role and content attributes.
    tags : List[str], optional
        List of tags for the conversation.
    expected_output : Optional[str], optional
        Expected output which will be used for correctness evaluation.
    rules : List[str], optional
        List of rules used for evaluation.
    demo_output : Optional[ChatMessage], optional
        Output of the agent for demonstration purposes.
    """

    messages: List[ChatMessage] = field(default_factory=list)
    rules: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    expected_output: Optional[str] = field(default=None)
    demo_output: Optional[ChatMessage] = field(default=None)

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
