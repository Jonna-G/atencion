import threading
import django
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
from core.mail import send_mail


class UserManager(BaseUserManager):

    def crearUsuario(self, nombre, apellido, email, direccion, telefono, password=None):
        
        if email is None:
            raise TypeError('Los usuarios deben tener un correo electrónico.')

        usuario = self.model(nombre=nombre, apellido=apellido, email=self.normalize_email(email), direccion=direccion, telefono=telefono)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

 
    def crearSuperUsuario(self, nombre, apellido, email, direccion, telefono, password):
        if password is None:
            raise TypeError('Los usuarios deben tener una contraseña.')

        usuario = self.crearUsuario(nombre, apellido, email, direccion, telefono, password)
        usuario.is_superuser = True
        usuario.is_staff = True
        usuario.save(using=self._db)
        return usuario

class User(AbstractUser, PermissionsMixin):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    cedula = models.IntegerField(("Cédula"), unique=True)
    email = models.EmailField(max_length=255, unique=True)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellido','cedula', 'direccion', 'telefono']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.nombre + ' ' + self.apellido + ' ' + self.cedula

    def get_short_name(self):
        return self.nombre

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)





