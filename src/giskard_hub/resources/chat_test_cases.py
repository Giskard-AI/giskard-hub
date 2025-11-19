from __future__ import annotations

from typing import List, Optional

from ..data._base import NOT_GIVEN
from ..data.chat import ChatMessage, ChatMessageWithMetadata
from ..data.chat_test_case import ChatTestCase, CheckConfig
from ._resource import APIResource
from ._utils import prepare_chat_test_case_data


class ChatTestCasesResource(APIResource):
    _base_url = "/v2/test-cases"

    def retrieve(self, chat_test_case_id: str):
        response = self._client.get(f"{self._base_url}/{chat_test_case_id}")
        return ChatTestCase.from_dict(response["data"], _client=self._client)

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

        response = self._client.post(
            self._base_url,
            json=data,
        )

        return ChatTestCase.from_dict(response["data"], _client=self._client)

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

        response = self._client.patch(
            f"{self._base_url}/{chat_test_case_id}",
            json=data,
        )

        return ChatTestCase.from_dict(response["data"], _client=self._client)

    def delete(self, chat_test_case_id: str | List[str]) -> None:
        if isinstance(chat_test_case_id, str):
            self._client.delete(f"{self._base_url}/{chat_test_case_id}")
            return
        self._client.delete(self._base_url, params={"test_case_ids": chat_test_case_id})

    def list(self, dataset_id: str) -> List[ChatTestCase]:
        response = self._client.get(f"/v2/datasets/{dataset_id}/test-cases")

        return [
            ChatTestCase.from_dict(item, _client=self._client)
            for item in response["data"]
        ]
