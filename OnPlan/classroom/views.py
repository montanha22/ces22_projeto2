
# Create your views here.

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from django.shortcuts import render

from allauth.socialaccount.models import SocialToken

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/classroom.student-submissions.me.readonly',
    ]
#SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly']
def show_courses(request):

    """Shows basic usage of the Classroom API.
    Prints the names of the first 10 courses the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('classroom', 'v1', credentials=creds)

    # Call the Classroom API
    results = service.courses().list(pageSize=10).execute()
    courses = results.get('courses', [])
    coursework = []
    #submissions = []
    tarefas = []
    i = 0
    for course in courses:
        results = service.courses().courseWork().list(courseId = course['id']).execute()
        coursework = results.get('courseWork',[])
        for work in coursework:
            date = work.get("dueDate",{})
            a = {
            'id':i,
            'titulo':work.get("title","Sem Titulo"),
            'materia':course.get("name","Sem Matéria"),
            'descrição':work.get("description","Sem Descrição"),
            'classroom':True,
            'dia_limite':date.get("day","Sem Dia de entrega"),
            'mes_limite':date.get("month","Sem Mês de entrega"),
            'ano_limite':date.get("year","Sem Ano de entrega"),
            }
            # results = service.courses().courseWork().studentSubmissions().list(courseId = course['id'], courseWorkId = work["id"]).execute()
            # submissions = results.get('studentSubmissions',[])
            # submission = submissions[-1]
            # b = {
            # 'atrasado': submission.get('late',False),
            # 'entregue': (submission.get('state','0') == "TURNED_IN" or submission.get('state','0') == "RETURNED"),
            # 'nota': submission.get('assignedGrade',-1),
            # }
            # a.update(b)
        tarefas.append(a)
        i = i+1

    return render(request, 'courses.html', {'courses': courses,'coursework' : coursework, 'tarefas': tarefas})