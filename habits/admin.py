# habits/admin.py
from django.contrib import admin
from .models import Habit, HabitTracking

admin.site.register(Habit)
admin.site.register(HabitTracking)