from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Q
from datetime import datetime, timedelta
from .models import Habit, HabitTracking
from .forms import HabitForm


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'تم إنشاء الحساب بنجاح!')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def dashboard(request):
    habits = Habit.objects.filter(user=request.user)
    today = timezone.now().date()
    
    # إحصائيات سريعة
    total_habits = habits.count()
    completed_today = HabitTracking.objects.filter(
        habit__user=request.user,
        date=today,
        completed=True
    ).count()
    
    # العادات الحديثة
    recent_habits = habits[:5]
    
    context = {
        'total_habits': total_habits,
        'completed_today': completed_today,
        'recent_habits': recent_habits,
        'today': today,
    }
    return render(request, 'habits/dashboard.html', context)


@login_required
def habit_list(request):
    habits = Habit.objects.filter(user=request.user)
    return render(request, 'habits/habit_list.html', {'habits': habits})


@login_required
def habit_create(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            messages.success(request, 'تم إنشاء العادة بنجاح!')
            return redirect('habit_list')
    else:
        form = HabitForm()
    return render(request, 'habits/habit_form.html', {'form': form, 'title': 'إضافة عادة جديدة'})


@login_required
def habit_edit(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث العادة بنجاح!')
            return redirect('habit_list')
    else:
        form = HabitForm(instance=habit)
    return render(request, 'habits/habit_form.html', {'form': form, 'title': 'تعديل العادة'})


@login_required
def habit_delete(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        habit.delete()
        messages.success(request, 'تم حذف العادة بنجاح!')
        return redirect('habit_list')
    return render(request, 'habits/habit_confirm_delete.html', {'habit': habit})


@login_required
def toggle_habit(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    today = timezone.now().date()
    
    tracking, created = HabitTracking.objects.get_or_create(
        habit=habit,
        date=today,
        defaults={'completed': True}
    )
    
    if not created:
        tracking.completed = not tracking.completed
        tracking.save()
    
    status = "مكتملة" if tracking.completed else "غير مكتملة"
    messages.success(request, f'تم تحديث حالة العادة إلى: {status}')
    return redirect('dashboard')


@login_required
def calendar_view(request):
    habits = Habit.objects.filter(user=request.user)
    today = timezone.now().date()
    
    # الحصول على آخر 30 يوم
    start_date = today - timedelta(days=29)
    tracking_data = HabitTracking.objects.filter(
        habit__user=request.user,
        date__gte=start_date,
        date__lte=today
    ).select_related('habit')
    
    # تنظيم البيانات حسب التاريخ
    calendar_data = {}
    for i in range(30):
        date = start_date + timedelta(days=i)
        calendar_data[date] = []
    
    for tracking in tracking_data:
        if tracking.date in calendar_data:
            calendar_data[tracking.date].append(tracking)
    
    context = {
        'habits': habits,
        'calendar_data': calendar_data,
        'today': today,
    }
    return render(request, 'habits/calendar.html', context)


@login_required
def analytics(request):
    habits = Habit.objects.filter(user=request.user)
    today = timezone.now().date()
    
    # إحصائيات عامة
    total_habits = habits.count()
    total_tracking = HabitTracking.objects.filter(habit__user=request.user).count()
    completed_tracking = HabitTracking.objects.filter(
        habit__user=request.user,
        completed=True
    ).count()
    
    completion_rate = 0
    if total_tracking > 0:
        completion_rate = round((completed_tracking / total_tracking) * 100, 1)
    
    # أفضل العادات (الأكثر إنجازاً)
    best_habits = habits.annotate(
        completed_count=Count('tracking_records', filter=Q(tracking_records__completed=True))
    ).order_by('-completed_count')[:5]
    
    context = {
        'total_habits': total_habits,
        'total_tracking': total_tracking,
        'completed_tracking': completed_tracking,
        'completion_rate': completion_rate,
        'best_habits': best_habits,
    }
    return render(request, 'habits/analytics.html', context)
