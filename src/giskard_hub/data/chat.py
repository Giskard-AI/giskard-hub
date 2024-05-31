from ._base import BaseData


from dataclasses import dataclass
from typing import Literal


@dataclass
class ChatMessage(BaseData):
    """Message from an LLM, with role & content."""

    role: Literal["system", "assistant", "user"]
    content: str
