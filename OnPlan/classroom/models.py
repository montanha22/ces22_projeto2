from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class tarefa_classroom(models.Model):
    titulo = models.CharField(max_length=400)
    materia = models.CharField(max_length=400)
    descrição = models.TextField()
    done = models.CharField(max_length=50,default='false')
    classroom = models.CharField(max_length=50,default='true')
    data_limite = models.CharField(max_length=400)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

class tarefa_personalizada(models.Model):
    titulo = models.CharField(max_length=400)
    materia = models.CharField(max_length=400)
    descrição = models.TextField()
    done = models.CharField(max_length=50,default='false')
    classroom = models.CharField(max_length=50,default='false')
    data_limite = models.CharField(max_length=400)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

class subject_table(models.Model):
    table = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE,default= None)