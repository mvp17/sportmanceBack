from django.urls import path
from dataAnalytics.views import GetDataToAnalyseView

urlpatterns = [
    path("get-analyzable-data", GetDataToAnalyseView.as_view()),
]
