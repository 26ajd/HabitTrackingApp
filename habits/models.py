from django.db import models
from django.contrib.auth.models import User


class Habit(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'يومي'),
        ('weekly', 'أسبوعي'),
        ('monthly', 'شهري'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    name = models.CharField(max_length=200, verbose_name='اسم العادة')
    description = models.TextField(blank=True, null=True, verbose_name='الوصف')
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='daily', verbose_name='التكرار')
    goal = models.IntegerField(blank=True, null=True, verbose_name='الهدف')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    
    class Meta:
        verbose_name = 'عادة'
        verbose_name_plural = 'العادات'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.user.username}"


class HabitTracking(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='tracking_records')
    date = models.DateField(verbose_name='التاريخ')
    completed = models.BooleanField(default=False, verbose_name='مكتملة')
    notes = models.TextField(blank=True, null=True, verbose_name='ملاحظات')
    
    class Meta:
        verbose_name = 'تتبع العادة'
        verbose_name_plural = 'تتبع العادات'
        unique_together = ['habit', 'date']  
        ordering = ['-date']
    
    def __str__(self):
        status = "مكتملة" if self.completed else "غير مكتملة"
        return f"{self.habit.name} - {self.date} - {status}"
