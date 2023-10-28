from django.urls import path
from eventsKeyWords.views import RegisterEventsKeyWordsView, GetPerformanceVariablesFromEventsFile

urlpatterns = [
    path("register-events-keywords", RegisterEventsKeyWordsView.as_view()),
    path("get-perform-vars-events-file", GetPerformanceVariablesFromEventsFile.as_view()),
]
