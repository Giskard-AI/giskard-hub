from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from ._base import BaseData


@dataclass
class ChatMessage(BaseData):
    """Message from an LLM, with role & content."""

    role: Literal["system", "assistant", "user"]
    content: str
