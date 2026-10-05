from django.db import models
from django.utils import timezone

class DailyRoutine(models.Model):
    date = models.DateField(default=timezone.now, unique=True)
    
    # 5 ta asosiy odat (Checkboxes)
    woke_up_early = models.BooleanField(default=False, verbose_name="05:00 da turdim")
    exercise_done = models.BooleanField(default=False, verbose_name="20-25 min mashq qildim")
    tax_code_read = models.BooleanField(default=False, verbose_name="Soliq kodeksi (30 min)")
    top_3_completed = models.BooleanField(default=False, verbose_name="3 ta muhim vazifa bajarildi")
    time_with_abdulloh = models.BooleanField(default=False, verbose_name="Abdulloh bilan vaqt (30-45 min)")
    
    # Qo'shimcha belgilashlar yoki eslatma
    notes = models.TextField(blank=True, null=True, verbose_name="Kunlik xulosa")

    @property
    def completion_percentage(self):
        tasks = [
            self.woke_up_early,
            self.exercise_done,
            self.tax_code_read,
            self.top_3_completed,
            self.time_with_abdulloh
        ]
        completed = sum(1 for task in tasks if task)
        return int((completed / len(tasks)) * 100)

    @property
    def status_color_class(self):
        pct = self.completion_percentage
        if pct < 40:
            return "bg-slate-800 text-slate-400 border-slate-700"  # Xira / To'q
        elif pct < 75:
            return "bg-amber-500 text-white shadow-md"             # O'rta (Sariq)
        elif pct < 90:
            return "bg-emerald-500 text-white shadow-lg"           # Yorqin yashil
        else:
            return "bg-green-400 text-emerald-950 shadow-green-500/50 shadow-2xl font-bold animate-pulse" # O'ta yorqin