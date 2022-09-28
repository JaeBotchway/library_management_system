from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="UserInfo"
    )
    gender = models.CharField(
        choices=[
            ("m", "Male"),
            ("f", "Female"),
        ],
        max_length=2,
        default="m",
        null=True
    )

    def __str__(self):
        return str(self.user.first_name)

    def validateEmail(self, email):
            try:
                validate_email(email)
                return True
            except ValidationError:
                return False

    @property
    def email(self):
        return self.user.email