from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class tarefa_classroom(models.Model):
    titulo = models.CharField(max_length=400)
    materia = models.CharField(max_length=400)
    descrição = models.CharField(max_length=10000)
    classroom = models.CharField(max_length=50)
    data_limite = models.CharField(max_length=400)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

class tarefa_personalizada(models.Model):
    titulo = models.CharField(max_length=400)
    materia = models.CharField(max_length=400)
    descrição = models.CharField(max_length=10000)
    classroom = models.CharField(max_length=50)
    data_limite = models.CharField(max_length=400)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)