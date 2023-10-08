from django.urls import path
from .views import RegisterSettingsView, GetInitAndFinTimesView

urlpatterns = [
    path("register-settings", RegisterSettingsView.as_view()),
    path("get-init-time_fin-time", GetInitAndFinTimesView.as_view())
]
