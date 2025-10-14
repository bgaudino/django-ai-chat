from enum import StrEnum
from typing import TypedDict


class Role(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(TypedDict):
    role: Role
    content: str


class Provider(StrEnum):
    OLLAMA = "ollama"
    OPENAI = "openai"
    GOOGLE = "google"


class Config(TypedDict):
    SYSYETM_PROMPT: Message
    PROVIDER: Provider
    MODEL: str
    API_KEY: str | None
    CHAT_TITLE: str | None
    PLACEHOLDER: str | None
