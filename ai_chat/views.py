from django.apps import apps
from django.core.cache import cache
from django.http import HttpResponse, StreamingHttpResponse, HttpResponseForbidden
from django.views.generic import FormView, View

from . import client, config
from .forms import ChatForm
from .templatetags.ai_chat_tags import safe_markdown
from .types import Message, Role


SESSION_KEY = "django_ai_chat_conversation"
CACHE_KEY = "django_ai_chat_system_prompt"


class LoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if config["LOGIN_REQUIRED"] and not request.user.is_authenticated:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


class ChatView(LoginRequiredMixin, FormView):
    form_class = ChatForm
    template_name = "ai_chat/_chat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conversation = self.get_conversation()
        if not conversation:
            conversation = []
            self.save_conversation(conversation)
        context["conversation"] = conversation
        context["config"] = config
        return context

    def form_valid(self, form):
        conversation = self.get_conversation()
        user_message = Message(
            role=Role.USER,
            content=form.cleaned_data["message"],
        )
        conversation.append(user_message)
        system_prompt = self.get_system_prompt()
        stream = client.chat(conversation, system_prompt)
        response = StreamingHttpResponse(
            self.stream_response(stream, conversation),
            content_type="text/event-stream",
        )
        return response

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context, status=400)

    def get_conversation(self):
        return self.request.session.get(SESSION_KEY, [])

    def save_conversation(self, conversation):
        self.request.session[SESSION_KEY] = conversation
        self.request.session.save()

    def get_system_prompt(self):
        cache_timeout = config.get("SYSTEM_PROMPT_CACHE_TIMEOUT")
        if apps.is_installed("ai_chat.prompts"):
            if cache_timeout:
                cached_prompt = cache.get(CACHE_KEY)
                if cached_prompt:
                    return cached_prompt

            from ai_chat.prompts.models import SystemPrompt

            if system_prompt := SystemPrompt.objects.first():
                if cache_timeout:
                    cache.set(CACHE_KEY, system_prompt.content, timeout=cache_timeout)
                return system_prompt.content

        return config.get("SYSTEM_PROMPT")

    def stream_response(self, stream, conversation):
        content = ""
        render_markdown = config["RENDER_MARKDOWN"]
        for chunk in stream:
            content += chunk
            yield safe_markdown(content) if render_markdown else content

        assistant_message = Message(
            role=Role.ASSISTANT,
            content=content,
        )
        conversation.append(assistant_message)
        self.save_conversation(conversation)


class ClearChatView(LoginRequiredMixin, View):
    def post(self, request):
        request.session[SESSION_KEY] = []
        return HttpResponse(status=204)
