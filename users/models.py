from django.db import models

# Create your models here.
# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # You can add more fields here in the future if you need them
    # For example: phone_number, date_of_birth, etc.
    email = models.EmailField(unique=True) # Making email the unique identifier is good practice

    def __str__(self):
        return self.username