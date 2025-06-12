from typing import Any, Dict, List, Optional, Union

from ..data._base import NOT_GIVEN, filter_not_given, maybe_to_dict
from ..data.chat import ChatMessage, ChatMessageWithMetadata
from ..data.chat_test_case import CheckConfig, TestCaseCheckConfig


def prepare_chat_test_case_data(
    dataset_id: str,
    messages: List[ChatMessage],
    demo_output: Optional[ChatMessageWithMetadata] = NOT_GIVEN,
    tags: Optional[List[str]] = None,
    checks: Optional[List[CheckConfig]] = None,
) -> dict[str, Any]:
    """Prepare the data for creating or updating a chat test case."""
    if tags is None:
        tags = []
    if checks is None:
        checks = []
    return filter_not_given(
        {
            "dataset_id": dataset_id,
            "messages": [maybe_to_dict(msg) for msg in messages],
            "demo_output": maybe_to_dict(demo_output),
            "tags": tags,
            "checks": [
                maybe_to_dict(check) for check in _format_checks_to_backend(checks)
            ],
        }
    )


def _format_checks_to_backend(
    checks: List[Union[CheckConfig, Dict[str, Any]]],
) -> List[TestCaseCheckConfig]:
    if not checks:
        return []

    checks = [check if isinstance(check, dict) else check.to_dict() for check in checks]

    return [
        TestCaseCheckConfig.from_dict(
            {
                "enabled": True,  # Default value for enabled
                **check,
                **(
                    {"assertions": [{"type": check["identifier"], **check["params"]}]}
                    if check.get("params")
                    else {}
                ),
            }
        )
        for check in checks
    ]
