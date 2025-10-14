from enum import StrEnum
from typing import TypedDict


class Role(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(TypedDict):
    role: Role
    content: str
