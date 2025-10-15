from abc import ABC, abstractmethod

from .types import Config, Message


class BaseProvider(ABC):
    def __init__(self, config: Config):
        self.config = config

    @abstractmethod
    def chat(self, messages: list[Message]):
        pass


class OllamaProvider(BaseProvider):
    def __init__(self, config: Config):
        super().__init__(config)
        from ollama import Client

        self.client = Client()

    def chat(self, messages: list[Message]):
        stream = self.client.chat(
            model=self.config["MODEL"],
            messages=[self.config["SYSTEM_PROMPT"]] + messages,
            stream=True,
        )
        for chunk in stream:
            yield chunk["message"]["content"]


class OpenAIProvider(BaseProvider):
    def __init__(self, config: Config):
        super().__init__(config)
        from openai import OpenAI

        self.client = OpenAI(api_key=self.config["API_KEY"])

    def chat(self, messages: list[Message]):
        stream = self.client.chat.completions.create(
            model=self.config["MODEL"],
            messages=[self.config["SYSTEM_PROMPT"]] + messages,
            max_tokens=self.config["MAX_TOKENS"],
            stream=True,
        )
        for chunk in stream:
            yield chunk.choices[0].delta.content or ""


class GoogleOpenAICompatibleProvider(OpenAIProvider):
    def __init__(self, config: Config):
        super().__init__(config)
        from openai import OpenAI

        self.client = OpenAI(
            api_key=self.config["API_KEY"],
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )


class GoogleProvider(BaseProvider):
    def __init__(self, config: Config):
        super().__init__(config)
        from google import genai

        self.client = genai.Client(api_key=self.config["API_KEY"])

    def _transform_messages(self, messages: list[Message]):
        from google.genai.types import Content

        contents: list[Content] = []
        for message in messages:
            if message["role"] == "system":
                continue
            contents.append(
                Content(
                    parts=[
                        {
                            "text": message["content"],
                        }
                    ],
                    role=message["role"] if message["role"] != "assistant" else "model",
                )
            )
        return contents

    def chat(self, messages: list[Message]):
        for chunk in self.client.models.generate_content_stream(
            model=self.config["MODEL"],
            contents=self._transform_messages(messages),
            config={
                "system_instruction": self.config["SYSTEM_PROMPT"]["content"],
                "max_output_tokens": self.config["MAX_TOKENS"],
            },
        ):
            yield chunk.text


class AnthropicProvider(BaseProvider):
    def __init__(self, config: Config):
        super().__init__(config)
        from anthropic import Anthropic

        self.client = Anthropic(api_key=self.config["API_KEY"])

    def chat(self, messages: list[Message]):
        stream = self.client.messages.create(
            max_tokens=self.config["MAX_TOKENS"],
            system=self.config["SYSTEM_PROMPT"]["content"],
            messages=messages,
            model=self.config["MODEL"],
            stream=True,
        )
        for event in stream:
            if event.type == "content_block_delta":
                yield event.delta.text
