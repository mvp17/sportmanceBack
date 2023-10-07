from django.urls import path
from .views import RegisterSettingsView, GetInitAndFinTimesView

urlpatterns = [
    path("settings", RegisterSettingsView.as_view()),
    path("init-time_fin-time", GetInitAndFinTimesView)
]
