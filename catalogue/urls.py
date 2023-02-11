from django.urls import path

from catalogue.views import main

urlpatterns = [
    path('/main/', main)
]