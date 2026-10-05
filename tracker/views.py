from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from .models import DailyRoutine

def routine_tracker(request):
    today = timezone.now().date()
    routine, created = DailyRoutine.objects.get_or_create(date=today)

    if request.method == "POST":
        routine.woke_up_early = 'woke_up_early' in request.POST
        routine.exercise_done = 'exercise_done' in request.POST
        routine.tax_code_read = 'tax_code_read' in request.POST
        routine.top_3_completed = 'top_3_completed' in request.POST
        routine.time_with_abdulloh = 'time_with_abdulloh' in request.POST
        routine.save()
        return redirect('routine_tracker')

    # Oxirgi 30 kunlik ma'lumotlarni olish
    start_date = today - timedelta(days=29)
    past_routines = DailyRoutine.objects.filter(date__gte=start_date, date__lte=today)
    
    # Sanalarni lug'atga aylantirish (tezkor qidirish uchun)
    routine_dict = {r.date: r for r in past_routines}

    # Oxirgi 30 kun uchun ro'yxat shakllantirish
    monthly_data = []
    for i in range(30):
        day = start_date + timedelta(days=i)
        day_routine = routine_dict.get(day)
        
        if day_routine:
            pct = day_routine.completion_percentage
            if pct == 0:
                bg_color = "bg-gray-800"
            elif pct < 40:
                bg_color = "bg-red-900/60"
            elif pct < 75:
                bg_color = "bg-amber-500"
            elif pct < 90:
                bg_color = "bg-emerald-500"
            else:
                bg_color = "bg-green-400 font-bold"
        else:
            pct = 0
            bg_color = "bg-gray-800/40"

        monthly_data.append({
            'date': day,
            'pct': pct,
            'bg_color': bg_color,
            'is_today': day == today
        })

    context = {
        'routine': routine,
        'monthly_data': monthly_data
    }

    return render(request, 'routine.html', context)