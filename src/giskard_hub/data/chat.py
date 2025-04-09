from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, Optional

from ._base import BaseData


@dataclass
class ChatMessage(BaseData):
    """Message from an LLM, with role & content."""

    role: Literal["system", "assistant", "user"]
    content: str


@dataclass
class ChatMessageWithMetadata(ChatMessage):
    metadata: Optional[dict[str, Any]] = None
