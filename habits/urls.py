from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('habits/', views.habit_list, name='habit_list'),
    path('habits/create/', views.habit_create, name='habit_create'),
    path('habits/<int:pk>/edit/', views.habit_edit, name='habit_edit'),
    path('habits/<int:pk>/delete/', views.habit_delete, name='habit_delete'),
    path('habits/<int:pk>/toggle/', views.toggle_habit, name='toggle_habit'),
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('analytics/', views.analytics, name='analytics'),
    path('register/', views.register, name='register'),
]

