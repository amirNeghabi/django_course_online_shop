# ai_assistant/urls.py
from django.urls import path
from . import views

app_name = "ai_assistant"

urlpatterns = [
    path("ask/", views.chat_widget, name="chat_widget"),
    path("history/", views.get_chat_history, name="chat_history"),
    path("clear/", views.clear_chat, name="clear_chat"),
]
