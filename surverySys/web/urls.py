from django.urls import path
from django.urls import include
from .views import basic

urlpatterns = [
    path("", basic.IndexView.as_view())
]
