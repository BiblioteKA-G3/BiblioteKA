from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    birthdate = models.DateField(null=True)
    loan_status = models.BooleanField(default=True)
    student = models.BooleanField(default=True)

    def __str__(self):
        return self.username
