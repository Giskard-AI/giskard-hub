from __future__ import annotations

import warnings
from typing import List, Optional

from ..data._base import NOT_GIVEN
from ..data.chat import ChatMessage, ChatMessageWithMetadata
from ..data.check import CheckConfig
from ..data.conversation import Conversation
from ._resource import APIResource
from ._utils import prepare_chat_test_case_data as prepare_conversation_data

_CONVERSATION_DEPRECATION_WARNING = "Conversation API is deprecated and will be removed. Please use ChatTestCase API instead."


class ConversationsResource(APIResource):
    def retrieve(self, conversation_id: str):
        warnings.warn(
            _CONVERSATION_DEPRECATION_WARNING,
            category=DeprecationWarning,
        )
        return self._client.get(
            f"/conversations/{conversation_id}", cast_to=Conversation
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
        warnings.warn(
            _CONVERSATION_DEPRECATION_WARNING,
            category=DeprecationWarning,
        )
        # pylint: disable=similarities
        # The `conversations` resource is deprecated and will be removed in the future.
        data = prepare_conversation_data(
            dataset_id=dataset_id,
            messages=messages,
            demo_output=demo_output,
            tags=tags,
            checks=checks,
        )

        return self._client.post(
            "/conversations",
            json=data,
            cast_to=Conversation,
        )

    # pylint: disable=too-many-arguments
    def update(
        self,
        conversation_id: str,
        *,
        dataset_id: str = NOT_GIVEN,
        messages: List[ChatMessage] = NOT_GIVEN,
        demo_output: Optional[ChatMessageWithMetadata] = NOT_GIVEN,
        tags: Optional[List[str]] = NOT_GIVEN,
        checks: Optional[List[CheckConfig]] = NOT_GIVEN,
    ) -> Conversation:
        warnings.warn(
            _CONVERSATION_DEPRECATION_WARNING,
            category=DeprecationWarning,
        )
        # pylint: disable=similarities
        # The `conversations` resource is deprecated and will be removed in the future.
        data = prepare_conversation_data(
            dataset_id=dataset_id,
            messages=messages,
            demo_output=demo_output,
            tags=tags,
            checks=checks,
        )

        return self._client.patch(
            f"/conversations/{conversation_id}",
            json=data,
            cast_to=Conversation,
        )

    def delete(self, conversation_id: str | List[str]) -> None:
        warnings.warn(
            _CONVERSATION_DEPRECATION_WARNING,
            category=DeprecationWarning,
        )
        return self._client.delete(
            "/conversations", params={"conversation_ids": conversation_id}
        )

    def list(self, dataset_id: str) -> List[Conversation]:
        warnings.warn(
            _CONVERSATION_DEPRECATION_WARNING,
            category=DeprecationWarning,
        )
        data = self._client.get(f"/datasets/{dataset_id}/conversations?limit=100000")
        return [
            Conversation.from_dict(d, _client=self._client)
            for d in data.get("items", [])
        ]
