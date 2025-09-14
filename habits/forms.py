from django import forms
from .models import Habit


class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'description', 'frequency', 'goal']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'اسم العادة'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'وصف العادة (اختياري)'
            }),
            'frequency': forms.Select(attrs={
                'class': 'form-select'
            }),
            'goal': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'الهدف (اختياري)',
                'min': 1
            }),
        }
        labels = {
            'name': 'اسم العادة',
            'description': 'الوصف',
            'frequency': 'التكرار',
            'goal': 'الهدف',
        }

