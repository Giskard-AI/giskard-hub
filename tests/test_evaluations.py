from giskard_hub.data.chat_test_case import ChatTestCase
from giskard_hub.data.conversation import Conversation
from giskard_hub.data.evaluation import EvaluationEntry
from giskard_hub.data.task import TaskStatus

TEST_CONVERSATION_DATA = {
    "id": "conv_123",
    "dataset_id": "ds_456",
    "messages": [
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi there! How can I help you?"},
    ],
    "demo_output": {
        "role": "assistant",
        "content": "This is a demo output.",
        "metadata": {"key": "value"},
    },
    "tags": ["greeting", "test"],
    "checks": [],
}


def test_evaluation_entry_from_chat_test_case():
    chat_test_case_data = TEST_CONVERSATION_DATA.copy()

    chat_test_case = ChatTestCase.from_dict(chat_test_case_data)
    evaluation_entry = EvaluationEntry.from_dict(
        {
            "chat_test_case": chat_test_case_data,
            "run_id": "run_123",
            "results": [],
            "status": TaskStatus.RUNNING,
            "model_output": None,
        }
    )

    assert isinstance(evaluation_entry.conversation, ChatTestCase)
    assert evaluation_entry.conversation.id == chat_test_case.id


def test_evaluation_entry_from_conversation():
    conversation_data = TEST_CONVERSATION_DATA.copy()

    conversation = Conversation.from_dict(conversation_data)
    evaluation_entry = EvaluationEntry.from_dict(
        {
            "conversation": conversation_data,
            "run_id": "run_123",
            "results": [],
            "status": TaskStatus.RUNNING,
            "model_output": None,
        }
    )

    assert isinstance(evaluation_entry.conversation, Conversation)
    assert evaluation_entry.conversation.id == conversation.id
