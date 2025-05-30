from giskard_hub.data.chat_test_case import ChatTestCase
from giskard_hub.data.conversation import Conversation


def test_consistency_between_conversations_and_chat_test_cases():
    dto = {
        "id": "conv_123",
        "dataset_id": "ds_456",
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
        "checks": [],
    }

    conversation = Conversation.from_dict(dto)
    chat_test_case = ChatTestCase.from_dict(dto)

    # Check messages
    assert len(chat_test_case.messages) == len(conversation.messages)
    for i in range(len(chat_test_case.messages)):
        assert chat_test_case.messages[i].role == conversation.messages[i].role
        assert chat_test_case.messages[i].content == conversation.messages[i].content

    # Check demo_output
    assert chat_test_case.demo_output.role == conversation.demo_output.role
    assert chat_test_case.demo_output.content == conversation.demo_output.content
    assert chat_test_case.demo_output.metadata == conversation.demo_output.metadata
    assert len(chat_test_case.demo_output.metadata) == len(
        conversation.demo_output.metadata
    )
    for key in chat_test_case.demo_output.metadata:
        assert key in conversation.demo_output.metadata
        assert (
            chat_test_case.demo_output.metadata[key]
            == conversation.demo_output.metadata[key]
        )

    # Check tags
    assert len(chat_test_case.tags) == len(conversation.tags)
    for tag in chat_test_case.tags:
        assert tag in conversation.tags

    # Check checks
    assert chat_test_case.checks == conversation.checks
    assert len(chat_test_case.checks) == len(conversation.checks)
    for i in range(len(chat_test_case.checks)):
        assert chat_test_case.checks[i].identifier == conversation.checks[i].identifier
        assert len(chat_test_case.checks[i].assertions) == len(
            conversation.checks[i].assertions
        )

    # Check common attributes
    assert chat_test_case.id == conversation.id
    assert chat_test_case.created_at == conversation.created_at
    assert chat_test_case.updated_at == conversation.updated_at
