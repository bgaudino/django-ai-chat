from django.conf import settings

from .types import Config


def get_ai_chat_config() -> Config:
    config = Config(**getattr(settings, "AI_CHAT", {}))
    if "PROVIDER" not in config:
        raise ValueError("AI_PROVIDER must be set in AI_CHAT configuration.")
    if "MODEL" not in config:
        raise ValueError("AI_MODEL must be set in AI_CHAT configuration.")
    config.setdefault("SYSTEM_PROMPT", None)
    config.setdefault("SYSTEM_PROMPT_CACHE_TIMEOUT", None)
    config.setdefault("MAX_TOKENS", 4096)
    config.setdefault("CHAT_TITLE", "Chat")
    config.setdefault("PLACEHOLDER", "Type your message here...")
    config.setdefault("LOGIN_REQUIRED", False)
    config.setdefault("RENDER_MARKDOWN", True)
    return config


config = get_ai_chat_config()

provider = config["PROVIDER"]
match provider:
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

        try:
            client = GoogleProvider(config)
        except ImportError:
            from .providers import GoogleOpenAICompatibleProvider

            client = GoogleOpenAICompatibleProvider(config)
    case "anthropic":
        from .providers import AnthropicProvider

        if "API_KEY" not in config:
            raise ValueError("API_KEY must be set in AI_CHAT configuration.")

        client = AnthropicProvider(config)
    case "mistral":
        from .providers import MistralProvider

        if "API_KEY" not in config:
            raise ValueError("API_KEY must be set in AI_CHAT configuration.")

        client = MistralProvider(config)
    case _:
        raise ValueError(
            f"Unsupported AI provider: {provider}. Supported providers: 'ollama, openai, google'."
        )
