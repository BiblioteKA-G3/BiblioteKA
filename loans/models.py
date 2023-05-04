from django.db import models


class Loan(models.Model):
    loan_date = models.DateField(auto_now_add=True)
    return_date = models.DateField()
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="users"
    )
    copy = models.ForeignKey(
        "copies.Copy", on_delete=models.CASCADE, related_name="copies"
    )

    def __str__(self) -> str:
        return f"{self.user} borrowed {self.copy}"
