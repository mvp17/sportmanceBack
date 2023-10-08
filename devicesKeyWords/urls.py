from django.urls import path
from .views import RegisterDevicesKeyWordsView, GetPerformanceVariablesFromDevicesFile

urlpatterns = [
    path("register-devices-keywords", RegisterDevicesKeyWordsView.as_view()),
    path("get-perform-vars-devices-file", GetPerformanceVariablesFromDevicesFile.as_view()),
]
