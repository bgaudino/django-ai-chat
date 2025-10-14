from django.conf import settings

from .types import Message, Role


def get_ai_chat_config():
    config = getattr(settings, "AI_CHAT", {})
    if "SYSTEM_PROMPT" not in config:
        raise ValueError("AI_SYSTEM_PROMPT must be set in AI_CHAT configuration.")
    elif isinstance(config["SYSTEM_PROMPT"], str):
        config["SYSTEM_PROMPT"] = Message(
            role=Role.SYSTEM,
            content=config["SYSTEM_PROMPT"],
        )
    if "PROVIDER" not in config:
        raise ValueError("AI_PROVIDER must be set in AI_CHAT configuration.")
    if "MODEL" not in config:
        raise ValueError("AI_MODEL must be set in AI_CHAT configuration.")
    return config


config = get_ai_chat_config()

provider = config.get("PROVIDER", "ollama")
if provider == "ollama":
    from .providers import OllamaProvider

    client = OllamaProvider(model=config["MODEL"])
elif provider == "openai":
    from .providers import OpenAIProvider
    if "OPENAI_API_KEY" not in config:
        raise ValueError("OPENAI_API_KEY must be set in AI_CHAT configuration.")

    client = OpenAIProvider(model=config["MODEL"], api_key=config["OPENAI_API_KEY"])
else:
    raise ValueError(
        f"Unsupported AI provider: {provider}. Supported providers: 'ollama, openai'."
    )
