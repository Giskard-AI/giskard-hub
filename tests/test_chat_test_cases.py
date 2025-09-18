from unittest.mock import MagicMock

import pytest

from giskard_hub.data.chat import ChatMessage, ChatMessageWithMetadata
from giskard_hub.data.chat_test_case import ChatTestCase
from giskard_hub.data.check import CheckConfig
from giskard_hub.errors import (
    HubAPIError,
    HubValidationError,
)
from giskard_hub.resources.chat_test_cases import ChatTestCasesResource


@pytest.fixture
def mock_client():
    mock_client = MagicMock()

    def mock_get(path, cast_to=None, **kwargs):
        data = mock_client.get.return_value
        if cast_to and data:
            return cast_to.from_dict(data)
        return data

    mock_client.get.side_effect = mock_get

    def mock_post(path, json=None, cast_to=None, **kwargs):
        data = mock_client.post.return_value
        if cast_to and data:
            return cast_to.from_dict(data)
        return data

    mock_client.post.side_effect = mock_post

    def mock_patch(path, json=None, cast_to=None, **kwargs):
        data = mock_client.patch.return_value
        if cast_to and data:
            return cast_to.from_dict(data)
        return data

    mock_client.patch.side_effect = mock_patch

    mock_client.delete.side_effect = lambda path, **kwargs: None

    return mock_client


@pytest.fixture
def mock_client_with_errors():
    mock_client = MagicMock()
    return mock_client


@pytest.fixture
def sample_chat_test_case_data():
    return {
        "id": "test_case_123",
        "created_at": "2025-06-17T12:46:52.424Z",
        "updated_at": "2025-06-17T12:46:52.424Z",
        "messages": [
            {
                "role": "user",
                "content": "Hello, how are you?",
            },
            {
                "role": "assistant",
                "content": "I'm fine, thank you!",
            },
        ],
        "demo_output": {
            "role": "assistant",
            "content": "I'm here to help you.",
            "metadata": {"source": "demo"},
        },
        "tags": ["greeting", "test"],
        "checks": [
            {
                "identifier": "conformity",
                "assertions": [
                    {"rules": ["The agent must be polite"], "type": "conformity"}
                ],
                "enabled": True,
            }
        ],
    }


@pytest.fixture
def sample_chat_test_cases_list_data():
    return {
        "items": [
            {
                "id": "test_case_123",
                "created_at": "2025-06-17T12:46:52.424Z",
                "updated_at": "2025-06-17T12:46:52.424Z",
                "messages": [
                    {
                        "role": "user",
                        "content": "Hello, how are you?",
                    },
                    {
                        "role": "assistant",
                        "content": "I'm fine, thank you!",
                    },
                ],
                "demo_output": {
                    "role": "assistant",
                    "content": "I'm here to help you.",
                    "metadata": {"source": "demo"},
                },
                "tags": ["greeting", "test"],
                "checks": [
                    {
                        "identifier": "conformity",
                        "type": "conformity",
                        "assertions": [
                            {
                                "rules": ["The agent must be polite"],
                                "type": "conformity",
                            }
                        ],
                        "enabled": True,
                    }
                ],
            },
            {
                "id": "test_case_456",
                "created_at": "2025-06-17T12:46:52.424Z",
                "updated_at": "2025-06-17T12:46:52.424Z",
                "messages": [
                    {
                        "role": "user",
                        "content": "What's the weather like?",
                    },
                ],
                "demo_output": None,
                "tags": ["weather"],
                "checks": [
                    {
                        "identifier": "conformity",
                        "type": "conformity",
                        "assertions": [
                            {
                                "rules": ["The agent must be polite"],
                                "type": "conformity",
                            }
                        ],
                        "enabled": True,
                    }
                ],
            },
        ]
    }


def test_chat_test_cases_list(mock_client, sample_chat_test_cases_list_data):
    mock_client.get.return_value = sample_chat_test_cases_list_data

    resource = ChatTestCasesResource(mock_client)
    result = resource.list(dataset_id="ds_456")

    assert mock_client.get.called
    mock_client.get.assert_called_once_with(
        "/datasets/ds_456/chat-test-cases?limit=100000"
    )

    assert isinstance(result, list)
    assert len(result) == 2

    # Check first chat test case
    first_case = result[0]
    assert isinstance(first_case, ChatTestCase)
    assert first_case.id == "test_case_123"
    assert len(first_case.messages) == 2
    assert first_case.messages[0].role == "user"
    assert first_case.messages[0].content == "Hello, how are you?"
    assert first_case.messages[1].role == "assistant"
    assert first_case.messages[1].content == "I'm fine, thank you!"
    assert first_case.demo_output.role == "assistant"
    assert first_case.demo_output.content == "I'm here to help you."
    assert first_case.demo_output.metadata == {"source": "demo"}
    assert first_case.tags == ["greeting", "test"]
    assert first_case.checks == [
        CheckConfig(
            identifier="conformity",
            params={"rules": ["The agent must be polite"], "type": "conformity"},
            enabled=True,
        )
    ]

    # Check second chat test case
    second_case = result[1]
    assert isinstance(second_case, ChatTestCase)
    assert second_case.id == "test_case_456"
    assert len(second_case.messages) == 1
    assert second_case.messages[0].content == "What's the weather like?"
    assert second_case.demo_output is None
    assert second_case.tags == ["weather"]
    assert second_case.checks == [
        CheckConfig(
            identifier="conformity",
            params={"rules": ["The agent must be polite"], "type": "conformity"},
            enabled=True,
        )
    ]


def test_chat_test_cases_retrieve(mock_client, sample_chat_test_case_data):
    mock_client.get.return_value = sample_chat_test_case_data

    resource = ChatTestCasesResource(mock_client)
    result = resource.retrieve(chat_test_case_id="test_case_123")

    assert mock_client.get.called
    mock_client.get.assert_called_once_with(
        "/chat-test-cases/test_case_123", cast_to=ChatTestCase
    )

    assert isinstance(result, ChatTestCase)
    assert result.id == "test_case_123"
    assert len(result.messages) == 2
    assert result.messages[0].role == "user"
    assert result.messages[0].content == "Hello, how are you?"
    assert result.demo_output.role == "assistant"
    assert result.demo_output.content == "I'm here to help you."
    assert result.tags == ["greeting", "test"]
    assert result.checks == [
        CheckConfig(
            identifier="conformity",
            params={"rules": ["The agent must be polite"], "type": "conformity"},
            enabled=True,
        )
    ]


def test_chat_test_cases_create(mock_client, sample_chat_test_case_data):
    mock_client.post.return_value = sample_chat_test_case_data

    resource = ChatTestCasesResource(mock_client)

    messages = [
        ChatMessage(role="user", content="Hello, how are you?"),
        ChatMessage(role="assistant", content="I'm fine, thank you!"),
    ]
    demo_output = ChatMessageWithMetadata(
        role="assistant",
        content="I'm here to help you.",
        metadata={"source": "demo"},
    )

    result = resource.create(
        dataset_id="ds_456",
        messages=messages,
        demo_output=demo_output,
        tags=["greeting", "test"],
        checks=[],
    )

    assert mock_client.post.called
    mock_client.post.assert_called_once_with(
        "/chat-test-cases",
        json={
            "dataset_id": "ds_456",
            "messages": [
                {"role": "user", "content": "Hello, how are you?"},
                {"role": "assistant", "content": "I'm fine, thank you!"},
            ],
            "demo_output": {
                "role": "assistant",
                "content": "I'm here to help you.",
                "metadata": {"source": "demo"},
            },
            "tags": ["greeting", "test"],
            "checks": [],
        },
        cast_to=ChatTestCase,
    )

    assert isinstance(result, ChatTestCase)
    assert result.id == "test_case_123"
    assert len(result.messages) == 2
    assert result.tags == ["greeting", "test"]


def test_chat_test_cases_create_minimal(mock_client):
    minimal_data = {
        "id": "test_case_minimal",
        "created_at": "2025-06-17T12:46:52.424Z",
        "updated_at": "2025-06-17T12:46:52.424Z",
        "messages": [
            {
                "role": "user",
                "content": "Simple question",
            },
        ],
        "demo_output": None,
        "tags": [],
        "checks": [],
    }

    mock_client.post.return_value = minimal_data

    resource = ChatTestCasesResource(mock_client)

    messages = [ChatMessage(role="user", content="Simple question")]

    result = resource.create(
        dataset_id="ds_456",
        messages=messages,
    )

    assert mock_client.post.called
    mock_client.post.assert_called_once_with(
        "/chat-test-cases",
        json={
            "dataset_id": "ds_456",
            "messages": [{"role": "user", "content": "Simple question"}],
            "demo_output": None,
            "tags": [],
            "checks": [],
        },
        cast_to=ChatTestCase,
    )

    assert isinstance(result, ChatTestCase)
    assert result.id == "test_case_minimal"
    assert len(result.messages) == 1
    assert result.demo_output is None
    assert result.tags == []


def test_chat_test_cases_update(mock_client, sample_chat_test_case_data):
    updated_data = {
        **sample_chat_test_case_data,
        "messages": [
            {
                "role": "user",
                "content": "Updated question: How are you doing?",
            },
            {
                "role": "assistant",
                "content": "I'm doing great, thanks for asking!",
            },
        ],
        "tags": ["greeting", "test", "updated"],
        "demo_output": {
            "role": "assistant",
            "content": "Updated demo output",
            "metadata": {"source": "updated_demo"},
        },
    }

    mock_client.patch.return_value = updated_data

    resource = ChatTestCasesResource(mock_client)

    new_messages = [
        ChatMessage(role="user", content="Updated question: How are you doing?"),
        ChatMessage(role="assistant", content="I'm doing great, thanks for asking!"),
    ]
    new_demo_output = ChatMessageWithMetadata(
        role="assistant",
        content="Updated demo output",
        metadata={"source": "updated_demo"},
    )

    result = resource.update(
        chat_test_case_id="test_case_123",
        messages=new_messages,
        demo_output=new_demo_output,
        tags=["greeting", "test", "updated"],
    )

    assert mock_client.patch.called
    mock_client.patch.assert_called_once_with(
        "/chat-test-cases/test_case_123",
        json={
            "messages": [
                {"role": "user", "content": "Updated question: How are you doing?"},
                {"role": "assistant", "content": "I'm doing great, thanks for asking!"},
            ],
            "demo_output": {
                "role": "assistant",
                "content": "Updated demo output",
                "metadata": {"source": "updated_demo"},
            },
            "tags": ["greeting", "test", "updated"],
        },
        cast_to=ChatTestCase,
    )

    assert isinstance(result, ChatTestCase)
    assert result.id == "test_case_123"
    assert len(result.messages) == 2
    assert result.messages[0].content == "Updated question: How are you doing?"
    assert result.demo_output.content == "Updated demo output"
    assert result.tags == ["greeting", "test", "updated"]


def test_chat_test_cases_update_partial(mock_client, sample_chat_test_case_data):
    updated_data = {
        **sample_chat_test_case_data,
        "tags": ["updated_tag"],
    }

    mock_client.patch.return_value = updated_data

    resource = ChatTestCasesResource(mock_client)

    result = resource.update(
        chat_test_case_id="test_case_123",
        tags=["updated_tag"],
    )

    assert mock_client.patch.called
    mock_client.patch.assert_called_once_with(
        "/chat-test-cases/test_case_123",
        json={
            "tags": ["updated_tag"],
        },
        cast_to=ChatTestCase,
    )

    assert isinstance(result, ChatTestCase)
    assert result.id == "test_case_123"
    assert result.tags == ["updated_tag"]


def test_chat_test_cases_delete_single(mock_client):
    resource = ChatTestCasesResource(mock_client)
    result = resource.delete(chat_test_case_id="test_case_123")

    assert mock_client.delete.called
    mock_client.delete.assert_called_once_with(
        "/chat-test-cases", params={"chat_test_case_ids": "test_case_123"}
    )

    assert result is None


def test_chat_test_cases_delete_multiple(mock_client):
    test_case_ids = ["test_case_123", "test_case_456", "test_case_789"]

    resource = ChatTestCasesResource(mock_client)
    result = resource.delete(chat_test_case_id=test_case_ids)

    assert mock_client.delete.called
    mock_client.delete.assert_called_once_with(
        "/chat-test-cases", params={"chat_test_case_ids": test_case_ids}
    )

    assert result is None


def test_chat_test_cases_list_empty_dataset(mock_client):
    mock_client.get.return_value = {"items": []}

    resource = ChatTestCasesResource(mock_client)
    result = resource.list(dataset_id="empty_dataset")

    assert mock_client.get.called
    mock_client.get.assert_called_once_with(
        "/datasets/empty_dataset/chat-test-cases?limit=100000"
    )

    assert isinstance(result, list)
    assert len(result) == 0


def test_chat_test_cases_retrieve_not_found_error(mock_client_with_errors):
    mock_client_with_errors.get.side_effect = HubAPIError(
        "Chat test case not found",
        status_code=404,
        response_text="Not Found",
    )

    resource = ChatTestCasesResource(mock_client_with_errors)

    with pytest.raises(HubAPIError) as exc_info:
        resource.retrieve(chat_test_case_id="nonexistent_test_case")

    assert exc_info.value.status_code == 404
    assert "Chat test case not found" in exc_info.value.message


def test_chat_test_cases_create_validation_error(mock_client_with_errors):
    mock_client_with_errors.post.side_effect = HubValidationError(
        "Validation error: Missing required fields\ndataset_id: This field is required\nmessages: This field is required",
        status_code=422,
        response_text="Unprocessable Entity",
    )

    resource = ChatTestCasesResource(mock_client_with_errors)

    with pytest.raises(HubValidationError) as exc_info:
        resource.create(
            dataset_id="",
            messages=[],
        )

    assert exc_info.value.status_code == 422
    assert "Missing required fields" in exc_info.value.message
    assert "dataset_id: This field is required" in exc_info.value.message
    assert "messages: This field is required" in exc_info.value.message


def test_chat_test_cases_update_not_found_error(mock_client_with_errors):
    mock_client_with_errors.patch.side_effect = HubAPIError(
        "Chat test case not found",
        status_code=404,
        response_text="Not found",
    )

    resource = ChatTestCasesResource(mock_client_with_errors)

    with pytest.raises(HubAPIError) as exc_info:
        resource.update(
            chat_test_case_id="nonexistent_test_case",
            tags=["new_tag"],
        )

    assert exc_info.value.status_code == 404
    assert "Chat test case not found" in exc_info.value.message
