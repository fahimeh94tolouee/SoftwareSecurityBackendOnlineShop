from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    credit_card = models.CharField(max_length=20, blank=True)
    signup_confirmed = models.BooleanField(default=False)
    otp_secret = models.CharField(max_length=16, blank=True)
    otp_sent_time = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
