from giskard_hub.data.chat import ChatMessage, ChatMessageWithMetadata


def test_chat_message_can_instantiate_from_dict():
    data = {"role": "assistant", "content": "Sorry, I cannot help you with that."}
    chat_message = ChatMessage.from_dict(data)
    assert chat_message.role == "assistant"
    assert chat_message.content == "Sorry, I cannot help you with that."


def test_chat_message_with_metadata_can_instantiate_from_dict():
    data = {
        "role": "assistant",
        "content": "Sorry, I cannot help you with that.",
        "metadata": {"key": "value"},
    }
    chat_message = ChatMessageWithMetadata.from_dict(data)
    assert chat_message.role == "assistant"
    assert chat_message.content == "Sorry, I cannot help you with that."
    assert chat_message.metadata == {"key": "value"}

    data = {
        "role": "assistant",
        "content": "Sorry, I cannot help you with that.",
    }
    chat_message = ChatMessageWithMetadata.from_dict(data)
    assert chat_message.role == "assistant"
    assert chat_message.content == "Sorry, I cannot help you with that."
    assert chat_message.metadata is None
