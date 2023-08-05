from typing import *

from tgtypes.user import User


class Message(Protocol):
    text: Optional[str]
    message_id: int
    from_user: Optional[User]
