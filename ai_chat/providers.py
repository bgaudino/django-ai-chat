class OllamaProvider:
    def __init__(self, model):
        from ollama import Client

        self.client = Client()
        self.model = model

    def chat(self, messages, stream=True):
        stream = self.client.chat(
            model=self.model,
            messages=messages,
            stream=stream,
        )
        for chunk in stream:
            yield chunk["message"]["content"]


class OpenAIProvider:
    def __init__(self, model, api_key):
        from openai import OpenAI

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def chat(self, messages, stream=True):
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=stream,
        )
        for chunk in stream:
            yield chunk.choices[0].delta.content or ""
