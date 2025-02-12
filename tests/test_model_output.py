from giskard_hub.data.model import ModelOutput


def test_model_output_can_instantiate_from_dict():
    # With message
    data = {
        "response": {
            "role": "user",
            "content": "Hello, how are you?",
        },
        "metadata": {"key": "value"},
    }
    model_output = ModelOutput.from_dict(data)
    assert model_output.message.content == "Hello, how are you?"
    assert model_output.error is None
    assert model_output.metadata == {"key": "value"}

    # With error
    data = {
        "metadata": {"meta1": "value1"},
        "error": {
            "message": "Error",
            "details": {"key": "value"},
        },
    }
    model_output = ModelOutput.from_dict(data)
    assert model_output.message is None
    assert model_output.error.message == "Error"
    assert model_output.error.details == {"key": "value"}
    assert model_output.metadata == {"meta1": "value1"}

    # Without metadata
    data = {
        "response": {
            "role": "user",
            "content": "Hello, how are you?",
        },
    }
    model_output = ModelOutput.from_dict(data)
    assert model_output.message.content == "Hello, how are you?"
    assert model_output.error is None
    assert model_output.metadata == {}
