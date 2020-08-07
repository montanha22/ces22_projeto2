
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
from classroom.models import tarefa_classroom, tarefa_personalizada

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/classroom.student-submissions.me.readonly',
    ]
#SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly']

def classroom_sync(request):
    
    user = request.user
    social_token = SocialToken.objects.get(account__user=request.user, account__provider = 'google')
    creds = Credentials(token=social_token.token,refresh_token=social_token.token_secret,client_id=social_token.app.client_id,client_secret=social_token.app.secret)

    service = build('classroom', 'v1', credentials=creds)

    #Delete Old activities

    tarefa_classroom.objects.filter(usuario=user).delete()

     # Call the Classroom API
    results = service.courses().list().execute()
    courses = results.get('courses', [])
    coursework = []
    #submissions = []
    tarefas = []
    i = 0
    for course in courses:
        if course["courseState"] == "ACTIVE":
            results = service.courses().courseWork().list(courseId = course['id']).execute()
            coursework = results.get('courseWork',[])
            for work in coursework:
                date = work.get("dueDate",{})
                time = work.get("dueTime",{})
                if time == {'hours': 2, 'minutes': 59}:
                    date = str(date.get("day")-1).zfill(2) + "/" + str(date.get("month","00")).zfill(2) + "/" + str(date.get("year","0000")).zfill(4)
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
                    id = str(i),
                    titulo = work.get("title","Sem Titulo"),
                    materia= course.get("name","Sem Matéria"),
                    descrição=work.get("description","Sem Descrição"), 
                    classroom= "true",
                    data_limite= date,
                    usuario = request.user
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
                i = i+1

    return redirect('/classroom/calendar')

def show_calendar(request):
    
    tc = list(tarefa_classroom.objects.filter(usuario=request.user).values())
    tp = list(tarefa_personalizada.objects.filter(usuario=request.user).values())
    
    if(tc == []):
        return redirect('/classroom/sincronizar')

    if(tp == []):
        tarefas = tc
    else:
        tarefas = tc.append(tp)

    return render(request, 'calendar.html', {'tarefas': tarefas})