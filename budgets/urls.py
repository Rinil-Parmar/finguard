from django.urls import path

from . import views

urlpatterns = [
    path('', views.budget_detail, name='budget_detail'),
    path('set/', views.budget_set, name='budget_set'),
]
