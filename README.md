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
from django.urls import include, path

urlpatterns = [
    # ...
    path("chat/", include("ai_chat.urls")),
]
```

Render the chat form somewhere in your page:

```html
{% include "ai_chat/chat.html" %}
```

## Configuration

You can configure Django AI Chat using the `AI_CHAT` dictionary in your Django settings.

---

`PROVIDER`:

Specifies which AI backend to use.
Supported values are `"openai"`, `"google"`, `"anthropic"`, `"mistral"`, and `"ollama"`.
This setting is **required**.

---

`MODEL`

Specifies the model to use for the selected provider. This setting is **required**.

---

`SYSTEM_PROMPT`

Defines the assistant’s behavior.
Set this to a string like `"You are a helpful assistant."`

---

`API_KEY`

Used for authentication with AI providers.
Not needed for Ollama, which runs locally, otherwise it is required.

---

`MAX_TOKENS`

Defines the maximum number of tokens the model can generate in a single response. Optional (default: 4096)

---

`CHAT_TITLE`

The text to display as a heading in the chat widget. Optional (default: "Chat")

---

`PLACEHOLDER`

The placeholder text for the message input. Optional (default: "Type your message here...")

---

`RENDER_MARKDOWN`

---

`PICO_THEME`

Sets the [PicoCSS](https://picocss.com) theme used by the chat widget.
Accepts `"light"` or `"dark"`, or `None` to use the browser’s preferred color scheme automatically.

---

`PICO_COLOR`

Specifies the [PicoCSS version](https://picocss.com/docs/version-picker) for the chat UI.
You can use any valid Pico color name (e.g. `"red"`, `"pink"`, `"fuchsia`).
If set to `None`, the default Pico color ("azure") will be used.

---

## Optional: Database-Stored System Prompt

Django AI Chat can optionally load the system prompt from the database if the `ai_chat.prompts` app is installed.

Add it to your project if you’d like to edit the system prompt from the Django admin instead of hard-coding it in settings:

```python
INSTALLED_APPS = [
    "ai_chat",
    "ai_chat.prompts",
]
```

Then run:

```bash
python manage.py migrate ai_chat.prompts
```

Once installed, the app provides a `SystemPrompt` model.
By default, the most recent prompt is used.
If you need to load prompts more dynamically you can subclass `ai_chat.views.ChatView` and override `get_system_prompt`.

`SYSTEM_PROMPT_CACHE_TIMEOUT`

If set, the system prompt (from the optional `ai_chat.prompts` app) will be cached for this many seconds.
If not set or None, caching is disabled and the prompt is read directly from the database each time.
