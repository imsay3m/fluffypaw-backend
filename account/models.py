from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class UserAccount(models.Model):
    user = models.OneToOneField(User, related_name="account", on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="images/profile",
        default="images/profile/user_avatar.png",
    )
    account_no = models.IntegerField(
        unique=True
    )  # account number will not be same for multiple user
    initial_deposite_date = models.DateField(auto_now_add=True)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.account_no}"


