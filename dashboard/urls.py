from django.urls import path
from views import GetChartData

urlpatterns = [
    path("get-chart-data", GetChartData.as_view()),
]
