import email
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils.safestring import mark_safe

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(blank=True, max_length=100)
    phone = models.CharField(blank=True, max_length=10)
    address = models.CharField(blank=True, max_length=550)
    city = models.CharField(blank=True, max_length=20)
    state = models.CharField(blank=True, max_length=50)
    pincode = models.CharField(blank=True, max_length=6)


    def __str__(self):
        return self.user.username

    def user_name(self):
        return self.user.username
