from abc import ABC, abstractmethod
from re import Pattern

from tgtypes.identities.chat_identity import ChatIdentity
from tgtypes.primitives import Username


class IChatResolver(ABC):
    @abstractmethod
    async def resolve_chat_by_username(self, username: Username) -> ChatIdentity:
        ...

    @abstractmethod
    async def resolve_chat_by_chat_id(self, chat_id: int) -> ChatIdentity:
        ...

    @abstractmethod
    async def resolve_chat_by_title_regex(self, title_regex: Pattern) -> ChatIdentity:
        ...
