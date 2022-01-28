from django.db import models
from django.contrib.auth.models import AbstractUser

#MODEL FOR FUNCTION BASED VIEW:

class CustomUser(AbstractUser):
    phone_no = models.CharField(max_length=10, null=True)
    dob = models.DateField(null=True)
    address = models.TextField(null=True)

    def __str__(self):
        return self.username
