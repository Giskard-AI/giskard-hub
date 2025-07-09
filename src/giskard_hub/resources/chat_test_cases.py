from __future__ import annotations

from typing import List, Optional

from ..data._base import NOT_GIVEN
from ..data.chat import ChatMessage, ChatMessageWithMetadata
from ..data.chat_test_case import ChatTestCase, CheckConfig
from ._resource import APIResource
from ._utils import prepare_chat_test_case_data


class ChatTestCasesResource(APIResource):
    def retrieve(self, chat_test_case_id: str):
        return self._client.get(
            f"/chat-test-cases/{chat_test_case_id}", cast_to=ChatTestCase
        )

    # pylint: disable=too-many-arguments
    def create(
        self,
        *,
        dataset_id: str,
        messages: List[ChatMessage],
        demo_output: Optional[ChatMessageWithMetadata] = None,
        tags: Optional[List[str]] = None,
        checks: Optional[List[CheckConfig]] = None,
    ):
        data = prepare_chat_test_case_data(
            dataset_id=dataset_id,
            messages=messages,
            demo_output=demo_output,
            tags=tags,
            checks=checks,
        )

        return self._client.post(
            "/chat-test-cases",
            json=data,
            cast_to=ChatTestCase,
        )

    # pylint: disable=too-many-arguments
    def update(
        self,
        chat_test_case_id: str,
        *,
        dataset_id: str = NOT_GIVEN,
        messages: List[ChatMessage] = NOT_GIVEN,
        demo_output: Optional[ChatMessageWithMetadata] = NOT_GIVEN,
        tags: Optional[List[str]] = NOT_GIVEN,
        checks: Optional[List[CheckConfig]] = NOT_GIVEN,
    ) -> ChatTestCase:
        data = prepare_chat_test_case_data(
            dataset_id=dataset_id,
            messages=messages,
            demo_output=demo_output,
            tags=tags,
            checks=checks,
        )

        return self._client.patch(
            f"/chat-test-cases/{chat_test_case_id}",
            json=data,
            cast_to=ChatTestCase,
        )

    def delete(self, chat_test_case_id: str | List[str]) -> None:
        return self._client.delete(
            "/chat-test-cases", params={"chat_test_case_ids": chat_test_case_id}
        )

    def list(self, dataset_id: str) -> List[ChatTestCase]:
        data = self._client.get(f"/datasets/{dataset_id}/chat-test-cases?limit=100000")
        return [
            ChatTestCase.from_dict(d, _client=self._client)
            for d in data.get("items", [])
        ]
