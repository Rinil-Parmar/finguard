from django.urls import path

from . import views

urlpatterns = [
    path('', views.history_detail, name='history_detail'),
]
