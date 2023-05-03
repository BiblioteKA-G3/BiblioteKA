from django.db import models


# Create your models here.
class Books(models.Model):
    class Meta:
        ordering = ["id"]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    pages = models.IntegerField()
    publisher = models.CharField(max_length=155)
    release_date = models.IntegerField()

    def __str__(self):
        return self.titulo
