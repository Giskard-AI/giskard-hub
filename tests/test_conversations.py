from unittest.mock import MagicMock

import pytest

from giskard_hub.data.chat import ChatMessage, ChatMessageWithMetadata
from giskard_hub.data.check import CheckConfig
from giskard_hub.data.conversation import Conversation
from giskard_hub.data.dataset import Dataset
from giskard_hub.resources.conversations import ConversationsResource


@pytest.fixture
def mock_client():
    mock_client = MagicMock()

    # POST
    mock_client.post.side_effect = lambda path, json=None, cast_to=None, **kwargs: (
        Conversation.from_dict(mock_client.post.return_value, _client=mock_client)
        if cast_to == Conversation
        else mock_client.post.return_value
    )

    # GET
    mock_client.get.side_effect = lambda path, cast_to=None, **kwargs: (
        Conversation.from_dict(mock_client.get.return_value, _client=mock_client)
        if cast_to == Conversation
        else mock_client.get.return_value
    )

    # PATCH
    mock_client.patch.side_effect = lambda path, json=None, cast_to=None, **kwargs: (
        Conversation.from_dict(mock_client.patch.return_value, _client=mock_client)
        if cast_to == Conversation
        else mock_client.patch.return_value
    )

    # DELETE
    mock_client.delete.side_effect = lambda path, **kwargs: None

    return mock_client


@pytest.fixture
def sample_conversation():
    return Conversation(
        messages=[
            ChatMessage(role="user", content="Hello, how can I help you?"),
            ChatMessage(role="assistant", content="I need help with my order."),
            ChatMessage(role="user", content="What's the issue with your order?"),
        ],
        demo_output=ChatMessageWithMetadata(
            role="assistant",
            content="My order #12345 hasn't arrived yet.",
            metadata={"order_id": "12345", "issue_type": "delivery"},
        ),
        tags=["customer-support", "order-issue"],
        checks=[
            CheckConfig(
                identifier="correctness",
                params={"reference": "I'll help you track your order."},
            ),
            CheckConfig(
                identifier="conformity",
                params={"rules": ["The assistant should be helpful and polite."]},
            ),
        ],
    )


def test_conversation_create(mock_client):
    """Test creating a conversation"""
    mock_client.post.return_value = {
        "id": "9c065c7d-421f-4fa1-aad3-902587837849",
        "created_at": "2025-05-20T09:46:52.424Z",
        "updated_at": "2025-05-20T09:46:52.424Z",
        "dataset_id": "23868ed8-d12f-40b1-8398-8df4cd066da3",
        "messages": [
            {"role": "user", "content": "Hello, how can I help you?"},
            {"role": "assistant", "content": "I need help with my order."},
            {"role": "user", "content": "What's the issue with your order?"},
        ],
        "demo_output": {
            "role": "assistant",
            "content": "My order #12345 hasn't arrived yet.",
            "metadata": {"order_id": "12345", "issue_type": "delivery"},
        },
        "tags": ["customer-support", "order-issue"],
        "checks": [
            {
                "identifier": "correctness",
                "assertions": [
                    {
                        "type": "correctness",
                        "reference": "I'll help you track your order.",
                    }
                ],
                "enabled": True,
            },
            {
                "identifier": "conformity",
                "assertions": [
                    {
                        "type": "conformity",
                        "rules": ["The assistant should be helpful and polite."],
                    }
                ],
                "enabled": True,
            },
        ],
        "comments": [],
    }

    messages = [
        ChatMessage(role="user", content="Hello, how can I help you?"),
        ChatMessage(role="assistant", content="I need help with my order."),
        ChatMessage(role="user", content="What's the issue with your order?"),
    ]

    demo_output = ChatMessageWithMetadata(
        role="assistant",
        content="My order #12345 hasn't arrived yet.",
        metadata={"order_id": "12345", "issue_type": "delivery"},
    )

    checks = [
        CheckConfig(
            identifier="correctness",
            params={"reference": "I'll help you track your order."},
        ),
        CheckConfig(
            identifier="conformity",
            params={"rules": ["The assistant should be helpful and polite."]},
        ),
    ]

    conversations_resource = ConversationsResource(mock_client)

    result = conversations_resource.create(
        dataset_id="23868ed8-d12f-40b1-8398-8df4cd066da3",
        messages=messages,
        demo_output=demo_output,
        tags=["customer-support", "order-issue"],
        checks=checks,
    )

    assert mock_client.post.called
    mock_client.post.assert_called_once()

    assert isinstance(result, Conversation)
    assert result.id == "9c065c7d-421f-4fa1-aad3-902587837849"
    assert len(result.messages) == 3
    assert result.messages[0].role == "user"
    assert result.messages[0].content == "Hello, how can I help you?"
    assert result.demo_output.content == "My order #12345 hasn't arrived yet."
    assert result.demo_output.metadata == {
        "order_id": "12345",
        "issue_type": "delivery",
    }
    assert "customer-support" in result.tags
    assert "order-issue" in result.tags
    assert len(result.checks) == 2
    assert result.checks[0].identifier == "correctness"
    assert result.checks[0].enabled
    assert result.checks[0].params == {
        "reference": "I'll help you track your order.",
        "type": "correctness",
    }
    assert result.checks[1].identifier == "conformity"
    assert result.checks[1].enabled
    assert result.checks[1].params == {
        "rules": ["The assistant should be helpful and polite."],
        "type": "conformity",
    }
    assert "comments" not in result.to_dict()


def test_conversation_retrieve(mock_client):
    """Test retrieving a conversation"""
    mock_client.get.return_value = {
        "id": "9c065c7d-421f-4fa1-aad3-902587837849",
        "created_at": "2025-05-20T09:46:52.424Z",
        "updated_at": "2025-05-20T09:46:52.424Z",
        "dataset_id": "23868ed8-d12f-40b1-8398-8df4cd066da3",
        "messages": [
            {"role": "user", "content": "Hello, what is the status of my last order?"}
        ],
        "demo_output": None,
        "tags": ["customer-support"],
        "checks": [],
        "comments": [],
    }

    conversations_resource = ConversationsResource(mock_client)

    result = conversations_resource.retrieve("9c065c7d-421f-4fa1-aad3-902587837849")

    assert mock_client.get.called
    mock_client.get.assert_called_once_with(
        "/conversations/9c065c7d-421f-4fa1-aad3-902587837849", cast_to=Conversation
    )

    assert isinstance(result, Conversation)
    assert result.id == "9c065c7d-421f-4fa1-aad3-902587837849"
    assert len(result.messages) == 1
    assert result.messages[0].role == "user"
    assert result.messages[0].content == "Hello, what is the status of my last order?"
    assert "customer-support" in result.tags
    assert len(result.checks) == 0
    assert "comments" not in result.to_dict()


def test_conversation_list(mock_client):
    """Test listing conversations"""
    mock_client.get.return_value = {
        "items": [
            {
                "id": "9c065c7d-421f-4fa1-aad3-902587837849",
                "created_at": "2025-05-20T09:46:52.424Z",
                "updated_at": "2025-05-20T09:46:52.424Z",
                "dataset_id": "23868ed8-d12f-40b1-8398-8df4cd066da3",
                "messages": [{"role": "user", "content": "Hello!"}],
                "demo_output": None,
                "tags": ["greeting"],
                "checks": [],
                "comments": [
                    {
                        "created_at": "2025-05-20T10:09:00.853Z",
                        "updated_at": "2025-05-20T10:09:00.853Z",
                        "uuid": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "comment": "string",
                        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "user_name": "string",
                    }
                ],
            },
            {
                "id": "87fcaf80-2244-43fe-8e1c-b1ba14ed1f2c",
                "created_at": "2025-05-20T09:46:52.424Z",
                "updated_at": "2025-05-20T09:46:52.424Z",
                "dataset_id": "23868ed8-d12f-40b1-8398-8df4cd066da3",
                "messages": [{"role": "user", "content": "Help me with my order."}],
                "demo_output": None,
                "tags": ["order-issue"],
                "checks": [],
                "comments": [],
            },
        ]
    }

    conversations_resource = ConversationsResource(mock_client)

    original_list_method = ConversationsResource.list

    def mock_list(self, dataset_id):
        data = self._client.get(f"/datasets/{dataset_id}/conversations?limit=100000")
        return [
            Conversation.from_dict(item, _client=self._client) for item in data["items"]
        ]

    ConversationsResource.list = mock_list

    try:
        results = conversations_resource.list("23868ed8-d12f-40b1-8398-8df4cd066da3")

        assert mock_client.get.called
        mock_client.get.assert_called_once_with(
            "/datasets/23868ed8-d12f-40b1-8398-8df4cd066da3/conversations?limit=100000"
        )

        assert len(results) == 2

        assert isinstance(results[0], Conversation)
        assert results[0].id == "9c065c7d-421f-4fa1-aad3-902587837849"
        assert results[0].messages[0].content == "Hello!"
        assert "greeting" in results[0].tags
        assert "comments" not in results[0].to_dict()

        assert isinstance(results[1], Conversation)
        assert results[1].id == "87fcaf80-2244-43fe-8e1c-b1ba14ed1f2c"
        assert "order-issue" in results[1].tags
        assert "comments" not in results[1].to_dict()
    finally:
        ConversationsResource.list = original_list_method


def test_conversation_update(mock_client):
    """Test updating a conversation"""
    mock_client.patch.return_value = {
        "id": "9c065c7d-421f-4fa1-aad3-902587837849",
        "created_at": "2025-05-20T09:46:52.424Z",
        "updated_at": "2025-05-20T09:46:52.424Z",
        "dataset_id": "23868ed8-d12f-40b1-8398-8df4cd066da3",
        "messages": [{"role": "user", "content": "Updated content!"}],
        "demo_output": None,
        "tags": ["updated-tag"],
        "checks": [
            {
                "identifier": "correctness",
                "assertions": [
                    {"type": "correctness", "reference": "Updated reference"}
                ],
                "enabled": True,
            }
        ],
    }

    conversations_resource = ConversationsResource(mock_client)

    new_messages = [ChatMessage(role="user", content="Updated content!")]
    new_tags = ["updated-tag"]
    new_checks = [
        CheckConfig(identifier="correctness", params={"reference": "Updated reference"})
    ]

    result = conversations_resource.update(
        conversation_id="9c065c7d-421f-4fa1-aad3-902587837849",
        messages=new_messages,
        tags=new_tags,
        checks=new_checks,
    )

    assert mock_client.patch.called

    assert isinstance(result, Conversation)
    assert result.id == "9c065c7d-421f-4fa1-aad3-902587837849"
    assert result.messages[0].content == "Updated content!"
    assert "updated-tag" in result.tags
    assert result.checks[0].identifier == "correctness"
    assert result.checks[0].params == {
        "reference": "Updated reference",
        "type": "correctness",
    }
    assert result.checks[0].enabled
    assert "comments" not in result.to_dict()


def test_conversation_delete(mock_client):
    """Test deleting a conversation"""

    conversations_resource = ConversationsResource(mock_client)

    conversations_resource.delete("9c065c7d-421f-4fa1-aad3-902587837849")

    mock_client.delete.assert_called_once_with(
        "/conversations",
        params={"conversation_ids": "9c065c7d-421f-4fa1-aad3-902587837849"},
    )

    mock_client.reset_mock()

    conversations_resource.delete(
        [
            "9c065c7d-421f-4fa1-aad3-902587837849",
            "87fcaf80-2244-43fe-8e1c-b1ba14ed1f2c",
        ]
    )

    mock_client.delete.assert_called_once_with(
        "/conversations",
        params={
            "conversation_ids": [
                "9c065c7d-421f-4fa1-aad3-902587837849",
                "87fcaf80-2244-43fe-8e1c-b1ba14ed1f2c",
            ]
        },
    )


def test_conversation_from_dict():
    """Test creating a Conversation from a dictionary"""
    data = {
        "id": "9c065c7d-421f-4fa1-aad3-902587837849",
        "messages": [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there"},
        ],
        "demo_output": {
            "role": "assistant",
            "content": "How can I help you?",
            "metadata": {"intent": "greeting"},
        },
        "tags": ["test-tag"],
        "checks": [
            {
                "identifier": "correctness",
                "assertions": [{"type": "correctness", "reference": "Hello world"}],
                "enabled": True,
            }
        ],
    }

    conversation = Conversation.from_dict(data)

    assert conversation.id == "9c065c7d-421f-4fa1-aad3-902587837849"
    assert len(conversation.messages) == 2
    assert conversation.messages[0].role == "user"
    assert conversation.messages[0].content == "Hello"
    assert conversation.demo_output.role == "assistant"
    assert conversation.demo_output.content == "How can I help you?"
    assert conversation.demo_output.metadata == {"intent": "greeting"}
    assert "test-tag" in conversation.tags
    assert conversation.checks[0].identifier == "correctness"
    assert conversation.checks[0].params == {
        "reference": "Hello world",
        "type": "correctness",
    }
    assert "dataset_id" not in conversation.to_dict()


def test_conversation_to_dict():
    """Test converting a Conversation to a dictionary"""
    data = {
        "id": "9c065c7d-421f-4fa1-aad3-902587837849",
        "dataset_id": "23868ed8-d12f-40b1-8398-8df4cd066da3",
        "created_at": "2025-05-20T09:46:52.424Z",
        "updated_at": "2025-05-20T09:46:52.424Z",
        "messages": [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there"},
        ],
        "demo_output": {
            "role": "assistant",
            "content": "How can I help you?",
            "metadata": {"intent": "greeting"},
        },
        "tags": ["test-tag"],
        "checks": [
            {
                "identifier": "correctness",
                "assertions": [{"type": "correctness", "reference": "Hello world"}],
                "enabled": True,
            }
        ],
    }
    conversation = Conversation.from_dict(data)

    result = conversation.to_dict()

    assert result["id"] == "9c065c7d-421f-4fa1-aad3-902587837849"
    assert len(result["messages"]) == 2
    assert result["messages"][0]["role"] == "user"
    assert result["messages"][0]["content"] == "Hello"
    assert result["demo_output"]["role"] == "assistant"
    assert result["demo_output"]["content"] == "How can I help you?"
    assert result["demo_output"]["metadata"] == {"intent": "greeting"}
    assert "test-tag" in result["tags"]
    assert result["checks"][0]["identifier"] == "correctness"
    assert result["checks"][0]["params"] == {
        "reference": "Hello world",
        "type": "correctness",
    }
    assert "dataset_id" not in result
    assert "comments" not in result


def test_dataset_conversations_property(mock_client):
    """Test accessing conversations through dataset property"""
    conversations_list = [
        Conversation.from_dict(
            {
                "id": "9c065c7d-421f-4fa1-aad3-902587837849",
                "messages": [{"role": "user", "content": "Hello!"}],
                "tags": ["greeting"],
            },
            _client=mock_client,
        )
    ]

    dataset = Dataset(name="Test Dataset")
    dataset.id = "23868ed8-d12f-40b1-8398-8df4cd066da3"

    mock_conversations = MagicMock(spec=ConversationsResource)
    mock_conversations.list.return_value = conversations_list

    mock_client.conversations = mock_conversations
    dataset._client = mock_client

    result = dataset.conversations

    mock_conversations.list.assert_called_once_with(
        dataset_id="23868ed8-d12f-40b1-8398-8df4cd066da3"
    )
    assert result == conversations_list


def test_create_conversation_through_dataset(mock_client):
    """Test creating a conversation through dataset method"""
    created_conversation = Conversation.from_dict(
        {
            "id": "9c065c7d-421f-4fa1-aad3-902587837849",
            "messages": [{"role": "user", "content": "Hello!"}],
            "tags": ["greeting"],
        },
        _client=mock_client,
    )

    dataset = Dataset(name="Test Dataset")
    dataset.id = "23868ed8-d12f-40b1-8398-8df4cd066da3"

    mock_conversations = MagicMock(spec=ConversationsResource)
    mock_conversations.create.return_value = created_conversation

    mock_client.conversations = mock_conversations
    dataset._client = mock_client

    conversation = Conversation(
        messages=[ChatMessage(role="user", content="Hello!")], tags=["greeting"]
    )

    result = dataset.create_conversation(conversation)

    mock_conversations.create.assert_called_once()
    call_kwargs = mock_conversations.create.call_args.kwargs
    assert "dataset_id" in call_kwargs
    assert call_kwargs["dataset_id"] == "23868ed8-d12f-40b1-8398-8df4cd066da3"
    assert result == created_conversation


def test_conversation_without_client():
    """Test that trying to access conversation methods without a client raises errors"""
    dataset = Dataset(name="Test Dataset")  # No client, no ID

    assert dataset.conversations is None

    conversation = Conversation(
        messages=[ChatMessage(role="user", content="Hello!")],
    )

    with pytest.raises(ValueError):
        dataset.create_conversation(conversation)
