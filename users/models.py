from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    birthdate = models.DateField(null=True)
    loan_status = models.BooleanField(default=True)
    student = models.BooleanField(default=True)
    blocked_date = models.DateField(null=True)

    follows_books = models.ManyToManyField(
        "books.Book",
        through="follows.Follow",
        related_name="user_followed"
    )

    def __str__(self):
        return self.username
