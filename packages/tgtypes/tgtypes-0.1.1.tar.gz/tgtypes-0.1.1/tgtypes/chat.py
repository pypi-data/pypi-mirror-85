from typing import Literal, Protocol


class Chat(Protocol):
    id: int
    type: Literal["private", "bot", "group", "supergroup", "channel"]
