from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

from giskard_hub.data.check import CheckConfig, TestCaseCheckConfig

from ._entity import Entity
from .chat import ChatMessage, ChatMessageWithMetadata


def _format_checks_to_cli(
    checks: List[Union[TestCaseCheckConfig, Dict[str, Any]]],
) -> List[CheckConfig]:
    if not checks:
        return []

    checks = [check if isinstance(check, dict) else check.to_dict() for check in checks]

    return [
        CheckConfig.from_dict(
            {
                "identifier": check["identifier"],
                "enabled": check["enabled"],
                **(
                    {"params": params}
                    if check.get("assertions")
                    and (
                        params := {
                            k: v
                            for k, v in check["assertions"][0].items()
                            if k != "type"
                        }
                    )
                    else {}
                ),
            }
        )
        for check in checks
    ]


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
    checks : List[TestCaseCheckConfig], optional
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
