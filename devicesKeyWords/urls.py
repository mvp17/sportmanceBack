from django.urls import path
from .views import DevicesKeyWordsView

urlpatterns = [
    path("devices-keywords", DevicesKeyWordsView.as_view()),
]
