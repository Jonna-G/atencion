import threading
import django
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
from alphapp.models.user import User
from core.mail import send_mail


class Paciente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    cedula = models.CharField(max_length=50, null=True, blank=True)

   

    def __str__(self):
        return self.usuario.email