from django.urls import path
from .views import EventsKeyWordsView

urlpatterns = [
    path("events-keywords", EventsKeyWordsView.as_view()),
]
