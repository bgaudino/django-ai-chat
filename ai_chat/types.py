from enum import StrEnum
from typing import Literal, TypedDict


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
    MISTRAL = "mistral"


class Config(TypedDict):
    SYSTEM_PROMPT: str | None
    SYSTEM_PROMPT_CACHE_TIMEOUT: int | None
    PROVIDER: Provider
    MODEL: str
    API_KEY: str | None
    MAX_TOKENS: int | None
    CHAT_TITLE: str | None
    PLACEHOLDER: str | None
    LOGIN_REQUIRED: bool
    RENDER_MARKDOWN: bool
    PICO_THEME: Literal["light", "dark"] | None
    PICO_COLOR: str | None
