from django.conf import settings

from .types import Config, Message, Role


def get_ai_chat_config():
    config = Config(**getattr(settings, "AI_CHAT", {}))
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

provider = config["PROVIDER"]
match config["PROVIDER"]:
    case "ollama":
        from .providers import OllamaProvider

        client = OllamaProvider(config)
    case "openai":
        from .providers import OpenAIProvider

        if "API_KEY" not in config:
            raise ValueError("API_KEY must be set in AI_CHAT configuration.")

        client = OpenAIProvider(config)
    case "google":
        from .providers import GoogleProvider

        if "API_KEY" not in config:
            raise ValueError("API_KEY must be set in AI_CHAT configuration.")

        client = GoogleProvider(config)
    case _:
        raise ValueError(
            f"Unsupported AI provider: {provider}. Supported providers: 'ollama, openai, google'."
        )
