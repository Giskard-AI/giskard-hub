from typing import Any, List, Optional

from giskard_hub.data.check import _format_checks_to_backend

from ..data._base import NOT_GIVEN, filter_not_given, maybe_to_dict
from ..data.chat import ChatMessage, ChatMessageWithMetadata
from ..data.chat_test_case import CheckConfig


def prepare_chat_test_case_data(
    dataset_id: str = NOT_GIVEN,
    messages: List[ChatMessage] = NOT_GIVEN,
    demo_output: Optional[ChatMessageWithMetadata] = NOT_GIVEN,
    tags: Optional[List[str]] = NOT_GIVEN,
    checks: Optional[List[CheckConfig]] = NOT_GIVEN,
) -> dict[str, Any]:
    """Prepare the data for creating or updating a chat test case."""

    if messages is not NOT_GIVEN:
        messages = [maybe_to_dict(msg) for msg in messages]
    if tags is None:
        tags = []
    if checks is None:
        checks = []
    if checks is not NOT_GIVEN:
        checks = [maybe_to_dict(check) for check in _format_checks_to_backend(checks)]

    return filter_not_given(
        {
            "dataset_id": dataset_id,
            "messages": messages,
            "demo_output": maybe_to_dict(demo_output),
            "tags": tags,
            "checks": checks,
        }
    )
