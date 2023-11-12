from django.urls import path
from dashboard.views import GetChartData

urlpatterns = [
    path("get-chart-data", GetChartData.as_view()),
]
