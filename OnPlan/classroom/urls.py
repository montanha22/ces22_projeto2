from django.urls import path
from . import views

urlpatterns = [
    #path('cursos',views.show_courses, name = 'show_courses'),
    path('calendar',views.show_calendar, name = 'show_calendar'),
    path('sincronizar',views.classroom_sync, name = 'classroom_sync'),
    path('salvaratividade',views.salvar_atividade, name = 'salvar_atividade'),
    path('excluiratividade',views.excluir_atividade, name = 'excluir_atividade'),
    path('completaratividade',views.completar_atividade, name = 'completar_atividade'),
    path('salvartabela',views.salvar_tabela, name = 'salvar_tabela'),
]