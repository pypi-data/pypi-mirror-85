import asyncio
import re
from typing import Dict, List, Optional, Pattern, Union

from pydantic import root_validator
from pydantic.dataclasses import dataclass

from tgtypes.descriptors.base import Descriptor
from tgtypes.identities.chat_identity import ChatIdentity
from tgtypes.interfaces.chatresolver import IChatResolver
from tgtypes.primitives import Username


@dataclass
class ChatDescriptor(Descriptor[ChatIdentity]):
    chat_id: Optional[int] = None
    username: Optional[Username] = None
    title_regex: Optional[Union[str, Pattern]] = None

    async def resolve(self, resolver: IChatResolver) -> ChatIdentity:
        identity = None

        try:
            if self.username and (
                identity := await resolver.resolve_chat_by_username(self.username)
            ):
                return identity

            if self.chat_id and (identity := await resolver.resolve_chat_by_chat_id(self.chat_id)):
                return identity

            if self.title_regex:
                if (
                    identity := await resolver.resolve_chat_by_title_regex(
                        re.compile(self.title_regex)
                    )
                ) :
                    return identity
        except Exception as ex:
            raise ValueError(f"Could not resolve chat identity of {self}.", self) from ex

        raise ValueError(f"Could not resolve chat identity of {self}.", self)

    @classmethod
    async def resolve_many(
        cls, resolver: IChatResolver, descriptors: List["ChatDescriptor"]
    ) -> List[ChatIdentity]:
        return list(await asyncio.gather(*[c.resolve(resolver) for c in descriptors]))

    @root_validator(skip_on_failure=True)
    def at_least_one(cls, v: Dict) -> Dict:  # TODO: make private and test
        if not any((v.values())):
            raise ValueError(f"Descriptors must specify at least one of their fields.")
        return v
