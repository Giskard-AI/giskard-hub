from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from giskard_hub.data.check import CheckConfig, _format_checks_to_cli

from ._entity import Entity
from .chat import ChatMessage, ChatMessageWithMetadata


@dataclass
class ChatTestCase(Entity):
    """A Dataset entry representing a chat test case.

    Attributes
    ----------
    messages : List[ChatMessage]
        List of messages in the chat test case. Each message is an object with a role and content attributes.
    demo_output : Optional[ChatMessageWithMetadata], optional
        Output of the agent for demonstration purposes.
    tags : List[str], optional
        List of tags for the chat test case.
    checks : List[CheckConfig], optional
        List of checks to be performed on the chat test case.
    """

    messages: List[ChatMessage] = field(default_factory=list)
    demo_output: Optional[ChatMessageWithMetadata] = field(default=None)
    tags: List[str] = field(default_factory=list)
    checks: List[CheckConfig] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> "ChatTestCase":
        # Process messages
        messages = []
        if data.get("messages"):
            messages = [ChatMessage.from_dict(msg) for msg in data["messages"]]

        # Process demo_output
        demo_output = None
        if data.get("demo_output"):
            demo_output = ChatMessageWithMetadata.from_dict(data["demo_output"])

        # Process checks
        checks = _format_checks_to_cli(data.get("checks", []))

        # Create the object with processed data
        obj = super().from_dict(
            {
                **data,
                "messages": messages,
                "demo_output": demo_output,
                "checks": checks,
            },
            **kwargs,
        )

        return obj
