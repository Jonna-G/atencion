from locale import normalize
import threading
import django
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
from alphapp.models.familiar import Familiar
from alphapp.models.medico import Medico
from alphapp.models.paciente import Paciente
from alphapp.models.user import User
from core.mail import send_mail

from django.core import mail
connection = mail.get_connection()

# Manually open the connection
connection.open()

# Construct an email message that uses the connection
email1 = mail.EmailMessage(
    'Hello',
    'Body goes here',
    'from@example.com',
    ['to1@example.com'],
    connection=connection,
)
email1.send() # Send the email

connection.send_messages([email1]) # Send both emails in the same connection
# The connection was already open so send_messages() doesn't close it.
# We need to manually close the connection.
connection.close()


class CrearUsuario(BaseUserManager):

    def __init__(self, nombre, apellido, cedula, email, direccion, telefono, password=None):
       
        self.nombre = nombre
        self.apellido = apellido
        self.cedula = cedula
        self.email = email
        self.direccion = direccion
        self.telefono = telefono
        self.password = password

    def run(self):
        if self.cedula is None:
            raise TypeError('Los usuarios deben tener una cedula.')

        usuario = User(nombre=self.nombre, apellido=self.apellido, cedula=self.cedula(self.cedula),email=self.email, direccion=self.direccion, telefono=self.telefono)
        usuario.set_password(self.password)
        usuario.save(using=self._db)
        return usuario

class ActualizarUsuario(BaseUserManager):
    def __init__(self, nombre, apellido, cedula, email, direccion, telefono, password=None):
       
        self.nombre = nombre
        self.apellido = apellido
        self.cedula = cedula
        self.email = email
        self.direccion = direccion
        self.telefono = telefono
        self.password = password

    def run(self):
        if self.cedula is None:
            raise TypeError('Actualiza Los usuarios deben tener una cedula.')

        usuario = User(nombre=self.nombre, apellido=self.apellido, cedula=self.cedula(self.cedula),email=self.email, direccion=self.direccion, telefono=self.telefono)
        usuario.set_password(self.password)
        usuario.save(using=self._db)
        return usuario

class BuscarUsuario(BaseUserManager):
    def __init__(self, cedula):
        
        self.cedula = cedula

    def run(self):
        if self.cedula is None:
            raise TypeError('Buscar Los usuarios deben tener una cedula.')

        usuario = User.objects.get(cedula=self.cedula)
        return usuario

class AsignarRol(BaseUserManager):
    def __init__(self, cedula, rol):
        
        self.cedula = cedula
        self.rol = rol

    def run(self):
        if self.cedula is None:
            raise TypeError('Asignar rol Los usuarios deben tener una cedula.')

        usuario = User.objects.get(cedula=self.cedula)
        usuario.rol = self.rol
        usuario.save(using=self._db)
        return usuario

class RolUsuario(BaseUserManager):
    def __init__(self, cedula):
        
        Familiar.objects.get(cedula=cedula)
        self.cedula = cedula

        Medico.objects.get(cedula=cedula)
        self.cedula = cedula

        Paciente.objects.get(cedula=cedula)
        self.cedula = cedula

    def run(self):
        if self.cedula is None:
            raise TypeError('Rol usuario, Los usuarios deben tener una cedula.')

        usuario = User.objects.get(cedula=self.cedula)
        return usuario



   
  