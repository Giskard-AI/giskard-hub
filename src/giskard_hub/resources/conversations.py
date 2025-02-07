from __future__ import annotations

from typing import List, Optional

from ..data._base import NOT_GIVEN, filter_not_given, maybe_to_dict
from ..data.chat import ChatMessage
from ..data.conversation import Conversation
from ._resource import APIResource


class ConversationsResource(APIResource):
    def retrieve(self, conversation_id: str):
        return self._client.get(
            f"/conversations/{conversation_id}", cast_to=Conversation
        )

    def create(
        self,
        *,
        dataset_id: str,
        messages: List[ChatMessage],
        rules: List[str] = NOT_GIVEN,
        tags: List[str] = NOT_GIVEN,
        expected_output: Optional[str] = NOT_GIVEN,
        demo_output: Optional[ChatMessage] = NOT_GIVEN,
    ):
        data = filter_not_given(
            {
                "dataset_id": dataset_id,
                "messages": [maybe_to_dict(msg) for msg in messages],
                "rules": rules,
                "tags": tags,
                "expected_output": expected_output,
                "demo_output": maybe_to_dict(demo_output),
            }
        )
        return self._client.post(
            "/conversations",
            json=data,
            cast_to=Conversation,
        )

    def update(
        self,
        conversation_id: str,
        *,
        dataset_id: str = NOT_GIVEN,
        messages: List[ChatMessage] = NOT_GIVEN,
        rules: List[str] = NOT_GIVEN,
        tags: List[str] = NOT_GIVEN,
        expected_output: Optional[str] = NOT_GIVEN,
        demo_output: Optional[ChatMessage] = NOT_GIVEN,
    ) -> Conversation:
        data = filter_not_given(
            {
                "dataset_id": dataset_id,
                "messages": (
                    [maybe_to_dict(msg) for msg in messages] if messages else messages
                ),
                "rules": rules,
                "tags": tags,
                "expected_output": expected_output,
                "demo_output": maybe_to_dict(demo_output),
            }
        )
        return self._client.patch(
            f"/conversations/{conversation_id}",
            json=data,
            cast_to=Conversation,
        )

    def delete(self, conversation_id: str | List[str]) -> None:
        return self._client.delete("/conversations", params={"conversation_ids": conversation_id})

    def list(self, dataset_id: str) -> List[Conversation]:
        data = self._client.get(f"/datasets/{dataset_id}/conversations?limit=100000")
        return [
            Conversation.from_dict(d, _client=self._client)
            for d in data.get("items", [])
        ]
