from django.urls import path
from session.views import GetSessionData, DeleteSessionData, ExitSession

urlpatterns = [
    path("get-session-data", GetSessionData.as_view()),
    path("exit-session", ExitSession.as_view()),
    path("delete-session-data", DeleteSessionData.as_view())
]
