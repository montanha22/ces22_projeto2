
# Create your views here.

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from django.shortcuts import render, redirect
import json
from allauth.socialaccount.models import SocialToken
from google.oauth2.credentials import Credentials
from classroom.models import tarefa_classroom, tarefa_personalizada, subject_table
from itertools import chain
import datetime

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/classroom.student-submissions.me.readonly',
    ]
#SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly']

def classroom_sync(request):

    try:
        social_token = SocialToken.objects.get(account__user=request.user, account__provider = 'google')
        creds = Credentials(token=social_token.token,refresh_token=social_token.token_secret,client_id=social_token.app.client_id,client_secret=social_token.app.secret)
        service = build('classroom', 'v1', credentials=creds)

        #Delete Old activities

        tarefa_classroom.objects.filter(usuario=request.user).delete()

        # Call the Classroom API
        results = service.courses().list().execute()
        courses = results.get('courses', [])
        coursework = []
        #submissions = []
        #tarefas = []
        
        for course in courses:
            if course["courseState"] == "ACTIVE":
                results = service.courses().courseWork().list(courseId = course['id']).execute()
                coursework = results.get('courseWork',[])
                for work in coursework:
                    date = work.get("dueDate",{})
                    time = work.get("dueTime",{})
                    if time == {'hours': 2, 'minutes': 59}:
                        date = str(date.get("day","00")).zfill(2) + "/" + str(date.get("month","00")).zfill(2) + "/" + str(date.get("year","0000")).zfill(4)
                        date = datetime.datetime.strptime(date,"%d/%m/%Y")
                        date = date - datetime.timedelta(days=1)
                        date = datetime.datetime.strftime(date,'%d/%m/%Y')
                    else:
                        date = str(date.get("day","00")).zfill(2) + "/" + str(date.get("month","00")).zfill(2) + "/" + str(date.get("year","0000")).zfill(4)
                    # a = {
                    # 'id':str(i),
                    # 'titulo':work.get("title","Sem Titulo"),
                    # 'materia':course.get("name","Sem Matéria"),
                    # 'descrição':work.get("description","Sem Descrição"),
                    # 'classroom':"true",
                    # 'data_limite':date,
                    # }
                    
                    nt = tarefa_classroom(
                        titulo = work.get("title","Sem Titulo"),
                        materia= course.get("name","Sem Matéria"),
                        descrição=work.get("description","Sem Descrição"), 
                        classroom= "true",
                        data_limite= date,
                        usuario = request.user,
                        done = 'false'
                    )
                    nt.save()
                    
                    # results = service.courses().courseWork().studentSubmissions().list(courseId = course['id'], courseWorkId = work["id"]).execute()
                    # submissions = results.get('studentSubmissions',[])
                    # submission = submissions[-1]
                    # b = {
                    # 'atrasado': submission.get('late',False),
                    # 'entregue': (submission.get('state','0') == "TURNED_IN" or submission.get('state','0') == "RETURNED"),
                    # 'nota': submission.get('assignedGrade',-1),
                    # }
                    # a.update(b)
                    # tarefas.append(a)

        return redirect('/classroom/calendar')

    except:
        return redirect('/accounts/logout')

def show_calendar(request):
    
    tc = list(tarefa_classroom.objects.filter(usuario=request.user).values())
    tp = list(tarefa_personalizada.objects.filter(usuario=request.user).values())

    tarefas = list(chain(tc,tp))

    table = subject_table.objects.filter(usuario = request.user).first()
    table = table.table
    return render(request, 'calendar.html', {'tarefas': tarefas, 'table': table})


def salvar_atividade(request):
    
    post = request.POST
    nt = tarefa_personalizada(
        titulo = post.get("titulo","Sem Titulo"),
        materia= post.get("materia","Sem Matéria"),
        descrição=post.get("descrição","Sem Descrição"), 
        classroom= "false",
        data_limite= post.get("data_limite","00/00/0000"),
        usuario = request.user,
        done = 'false'
    )
    nt.save()

    return redirect('/classroom/calendar')


def excluir_atividade(request):

    post = request.POST
    print('flkdjgflkfjlkj')
    if post.get("classroom") == 'true':
        tarefa = tarefa_classroom.objects.filter(materia=post.get("materia"),titulo=post.get("titulo"),usuario=request.user)
    else:
        tarefa = tarefa_personalizada.objects.filter(materia=post.get("materia"),titulo=post.get("titulo"),usuario=request.user)
    print(tarefa)
    tarefa.delete()

    return redirect('/classroom/calendar')

def completar_atividade(request):

    post = request.POST

    if post.get("classroom") == 'true':
        tarefa = tarefa_classroom.objects.filter(materia=post.get("materia"),titulo=post.get("titulo"),usuario=request.user)
    else:
        tarefa = tarefa_personalizada.objects.filter(materia=post.get("materia"),titulo=post.get("titulo"),usuario=request.user)

    tarefa.update(done=post.get('done'))

    return redirect('/classroom/calendar')

def salvar_tabela(request):

    post = request.POST
    subject_table.objects.filter(usuario=request.user).delete()

    nt = subject_table(
        table = post.get('table'),
        usuario = request.user
    )
    nt.save()

    return redirect('/classroom/calendar')
    
