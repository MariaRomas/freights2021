from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Пользователи"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_customer = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)
    

    def __str__(self):
        return self.first_name




class Customer(models.Model):
    """Грузовладельцы"""
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    phone_number = models.CharField( max_length=20)
    location = models.CharField(max_length=20)
    company = models.CharField(max_length=20,  default="none")
    def __str__(self):
        return self.company

class Driver(models.Model):
    """Грузоперевозчики"""
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    phone_number = models.CharField(max_length=20)
    designation = models.CharField(max_length=20)
    company = models.CharField(max_length=20, default="none")
    def __str__(self):
        return self.company