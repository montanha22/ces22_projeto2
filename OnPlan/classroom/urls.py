from django.urls import path
from . import views

urlpatterns = [
    #path('cursos',views.show_courses, name = 'show_courses'),
    path('calendar',views.show_calendar, name = 'show_calendar'),
]