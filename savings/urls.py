from django.urls import path

from . import views

urlpatterns = [
    path('', views.savings_goal_list, name='savings_goal_list'),
    path('add/', views.savings_goal_create, name='savings_goal_create'),
    path('<int:pk>/edit/', views.savings_goal_update, name='savings_goal_update'),
    path('<int:pk>/add-saving/', views.savings_goal_add_contribution, name='savings_goal_add_contribution'),
    path('<int:pk>/complete/', views.savings_goal_complete, name='savings_goal_complete'),
    path('<int:pk>/delete/', views.savings_goal_delete, name='savings_goal_delete'),
]
