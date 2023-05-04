from django.db import models


class Follow(models.Model):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="followed_by"
    )
    book = models.ForeignKey(
        "books.Book", on_delete=models.CASCADE, related_name="follows"
    )

    def __str__(self) -> str:
        return f"{self.user} is following {self.book}"
