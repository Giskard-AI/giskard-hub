from __future__ import annotations

import warnings
from dataclasses import dataclass
from typing import Any, Dict

from .chat_test_case import ChatTestCase


@dataclass
class Conversation(ChatTestCase):
    """A Dataset entry representing a conversation.

    Attributes
    ----------
    messages : List[ChatMessage]
        List of messages in the conversation. Each message is an object with a role and content attributes.
    demo_output : Optional[ChatMessageWithMetadata], optional
        Output of the agent for demonstration purposes.
    tags : List[str], optional
        List of tags for the conversation.
    checks : List[CheckConfig], optional
        List of checks to be performed on the conversation.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> "Conversation":
        warnings.warn(
            "Conversation is deprecated and will be removed. Please use ChatTestCase instead.",
            category=DeprecationWarning,
        )
        return super().from_dict(data, **kwargs)
