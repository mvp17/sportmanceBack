from django.urls import path
from dataInput.views import RegisterDataInput, DeleteDataInput

urlpatterns = [
    path("register-data-input", RegisterDataInput.as_view()),
    path("delete-data-input/<int:pk>", DeleteDataInput.as_view()),
]
