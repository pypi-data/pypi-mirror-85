from typing import Optional, Protocol, Union, runtime_checkable
from warnings import warn

from pydantic import ValidationError
from pydantic.dataclasses import dataclass

from tgtypes.chat import Chat


@runtime_checkable
class _MessageUpdate(Protocol):
    chat: Chat
    message_id: int


@runtime_checkable
class _AnyUpdateWithMessageProperty(Protocol):
    message: _MessageUpdate


@runtime_checkable
class _ChosenInlineResultUpdate(Protocol):
    inline_message_id: str


@runtime_checkable
class _CallbackQueryUpdate(Protocol):
    inline_message_id: str


@dataclass(frozen=True)
class MessageIdentity:

    # TODO: Make this a ChatIdentity !!!
    chat_id: Optional[Union[int, str]]  # will be None for inline messages

    message_id: Union[int, str]
    is_inline: bool
    is_deleted: bool = False  # TODO: implement

    @classmethod
    def from_update(
        cls, update: Union[_MessageUpdate, _CallbackQueryUpdate]
    ) -> Optional["MessageIdentity"]:
        if isinstance(update, _MessageUpdate):
            return cls.from_message(update)
        elif isinstance(update, _CallbackQueryUpdate) and update.inline_message_id:
            return MessageIdentity(
                chat_id=None, message_id=update.inline_message_id, is_inline=True,
            )
        elif isinstance(update, _AnyUpdateWithMessageProperty) and update.message:
            return cls.from_message(update.message)

        return None

    @classmethod
    def from_message(cls, message: _MessageUpdate):
        return MessageIdentity(
            chat_id=message.chat.id, message_id=message.message_id, is_inline=False
        )

    @classmethod
    def from_chosen_inline_result(
        cls, update: _ChosenInlineResultUpdate, chat_id: int
    ) -> Optional["MessageIdentity"]:
        # TODO: consider removing
        try:
            return MessageIdentity(
                chat_id=chat_id, message_id=update.inline_message_id, is_inline=True
            )
        except ValidationError:
            warn("Could not extract message identity from chosen inline result.")
            return None


# @dataclass(unsafe_hash=True)
# class MessageIdentity:
#     chat_id: int
#     message_id: int
#     client_user_id: int
#
#     @classmethod
#     async def from_message(
#         cls, message: Union[view_sender_interface, "MessageIdentity"], client: ConfiguredClient = None
#     ) -> "MessageIdentity":
#         if isinstance(message, MessageIdentity):
#             return message
#         if not client:
#             client = message._client
#
#         # debug
#         if message.chat is None:
#             print("No chatid in this type:", type(message))
#             return
#
#         try:
#             return MessageIdentity(
#                 chat_id=message.chat.id,
#                 message_id=message.message_id,
#                 client_user_id=(await client.get_me()).id,
#             )
#         except Exception as ex:
#             print(message)
#             raise ex
