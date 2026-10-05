from django.contrib import admin
from django.urls import path
from tracker.views import routine_tracker

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', routine_tracker, name='routine_tracker'),
]