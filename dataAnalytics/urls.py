from django.urls import path
from views import GetDataToAnalyseView

urlpatterns = [
    path("get-analyzable-data", GetDataToAnalyseView.as_view()),
]
