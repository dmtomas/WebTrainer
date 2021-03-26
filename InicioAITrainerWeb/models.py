from django.db import models


# Create your models here.
class Clases_Curso(models.Model):
    titulo = models.CharField(max_length=64)
    descripcion = models.CharField(max_length=1024)
