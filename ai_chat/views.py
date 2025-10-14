from django.http import HttpResponse, StreamingHttpResponse
from django.views.generic import FormView, View

from . import client, config
from .forms import ChatForm
from .types import Message, Role


SESSION_KEY = "django_ai_chat_conversation"


class ChatView(FormView):
    form_class = ChatForm
    template_name = "ai_chat/_chat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conversation = self.get_conversation()
        if not conversation:
            conversation = []
            self.save_conversation(conversation)
        context["conversation"] = conversation
        return context

    def form_valid(self, form):
        conversation = self.get_conversation()
        user_message = Message(
            role=Role.USER,
            content=form.cleaned_data["message"],
        )
        conversation.append(user_message)
        stream = self.chat(conversation)
        response = StreamingHttpResponse(
            self.stream_response(stream, conversation),
            content_type="text/event-stream",
        )
        return response

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context, status=400)

    def chat(self, conversation):
        return client.chat([config["SYSTEM_PROMPT"]] + conversation)

    def get_conversation(self):
        return self.request.session.get(SESSION_KEY, [])

    def save_conversation(self, conversation):
        self.request.session[SESSION_KEY] = conversation
        self.request.session.save()

    def stream_response(self, stream, conversation):
        assistant_message = Message(
            role=Role.ASSISTANT,
            content="",
        )
        for chunk in stream:
            yield chunk
            assistant_message["content"] += chunk

        conversation.append(assistant_message)
        self.save_conversation(conversation)


class ClearChatView(View):
    def post(self, request):
        request.session[SESSION_KEY] = []
        return HttpResponse(status=204)
