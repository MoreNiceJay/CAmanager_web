from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    email_authenticated = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=16,blank=True)
    phone_number_authenticated = models.BooleanField(default=True)


    