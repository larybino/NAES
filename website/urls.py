from django.urls import path, include
from .views import AboutView, IndexView, ContatoView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("about/", AboutView.as_view(), name="about"),
]