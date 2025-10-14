# Django AI Chat

A lightweight, drop-in Django app for embedding an AI-powered chat widget into your site.

## Quick start

Add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    "ai_chat",
]
```

Add an `AI_CHAT` dictionary to your Django settings:

```python
AI_CHAT = {
    "PROVIDER": "openai",
    "MODEL": "gpt-4o-mini",
    "API_KEY": "",
    "SYSTEM_PROMPT": "You are a helpful assistant.",
}
```

In your `urls.py`:

```python
from django.urls import include

urlpatterns = [
    # ...
    path("chat/", include("aichat.urls"),
]
```

Render the chat form somewhere in your page:

```html
{% include "ai_chat/chat.html" %}
```

## Configuration

You can configure Django AI Chat using the `AI_CHAT` dictionary in your Django settings.

---

### `PROVIDER`:

Specifies which AI backend to use.
Supported values are `"openai"`, `"google"`, and `"ollama"`.
This setting is **required**.

---

### `MODEL`

Specifies the model to use for the selected provider. This setting is **required**.

---

### `SYSTEM_PROMPT`

Defines the assistant’s behavior.
Set this to a string like `"You are a helpful assistant."`. This setting is **required**.

---

### `API_KEY`

Used for authentication with AI providers.
Not needed for Ollama, which runs locally, otherwise it is required.

---

### `CHAT_TITLE`

The text to display as a heading in the chat widget. Optional (default: "Chat")

---

### `PLACEHOLDER`

The placeholder text for the message input. Optional (default: "Type your message here...")
