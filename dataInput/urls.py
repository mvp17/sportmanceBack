from django.urls import path
from .views import DataInputView

urlpatterns = [
    path("data-input", DataInputView.as_view()),
]
