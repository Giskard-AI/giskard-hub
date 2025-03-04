from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ._base import BaseData
from ._entity import Entity
from .chat import ChatMessage


def _format_checks_to_cli(checks: List[TestCaseCheckConfig]) -> List[CheckConfig]:
    return [
        {
            "identifier": check["identifier"],
            "enabled": check["enabled"],
            **(
                {"params": params}
                if check.get("assertions")
                and (
                    params := {
                        k: v for k, v in check["assertions"][0].items() if k != "type"
                    }
                )
                else {}
            ),
        }
        for check in checks
    ]


@dataclass
class CheckConfig(BaseData):
    identifier: str
    params: Optional[dict[str, Any]] = None


@dataclass
class TestCaseCheckConfig(BaseData):
    identifier: str
    assertions: List[dict[str, Any]]


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
    checks : List[TestCaseCheckConfig], optional
        List of checks to be performed on the conversation.
    """

    messages: List[ChatMessage] = field(default_factory=list)
    demo_output: Optional[ChatMessage] = field(default=None)
    tags: List[str] = field(default_factory=list)
    checks: List[TestCaseCheckConfig] = field(default_factory=list)

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
        obj.checks = _format_checks_to_cli(obj.checks)
        return obj
