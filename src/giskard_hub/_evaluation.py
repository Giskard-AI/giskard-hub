from typing import Callable, List

from .data.chat import ChatMessage
from .data.model import ModelOutput


class LocalModel:
    def __init__(self, *, name: str, description: str):
        self.name = name
        self.description = description

    def __call__(self, messages: List[ChatMessage], **kwargs) -> ModelOutput:
        raise NotImplementedError(
            "This method needs to be implemented by the subclass."
        )

    @staticmethod
    def from_callable(callable: Callable) -> "LocalModel":
        return CallableLocalModel(
            name=callable.__name__,
            description=callable.__doc__ or "",
            callable=_validate_callable(callable),
        )


class CallableLocalModel(LocalModel):
    def __init__(
        self,
        *,
        name,
        description,
        callable: Callable,
    ):
        super().__init__(name=name, description=description)
        self._callable = callable

    def __call__(self, messages: List[ChatMessage], **kwargs) -> ModelOutput:
        output = self._callable(messages, **kwargs)

        if isinstance(output, ModelOutput):
            return output

        return ModelOutput(message=ChatMessage(role="assistant", content=str(output)))


def _validate_callable(callable: Callable) -> Callable:
    if not callable.__name__:
        raise ValueError("The callable needs to have a name.")

    return callable
