from django.db import models


class Copy(models.Model):
    copy_count = models.IntegerField()

    book = models.OneToOneField(
        "books.Book", on_delete=models.CASCADE, related_name="copies"
    )

    def __str__(self) -> str:
        return f"{self.book} - copy {self.copy_count}"
