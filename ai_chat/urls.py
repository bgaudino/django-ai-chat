from django.urls import path

from . import views


urlpatterns = [
    path("", views.ChatView.as_view(), name="chat"),
    path("clear/", views.ClearChatView.as_view(), name="clear_chat"),
]
