from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from django.contrib.auth.models import Group
from .models import User, Customer, Driver


class CustomerSignUpForm(UserCreationForm):
    Имя = forms.CharField(required=True)
    Фамилия = forms.CharField(required=True)
    Номер_телефона = forms.CharField(required=True)
    Местоположение = forms.CharField(required=True)
    
  

    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.is_staff = True
        user.first_name = self.cleaned_data.get('Имя')
        user.last_name = self.cleaned_data.get('Фамилия')
        user.save()
        group = Group.objects.get(name='customers')
        user.groups.add(group)
        user.save()
        customer = Customer.objects.create(user=user)
        customer.phone_number=self.cleaned_data.get('Номер_телефона')
        customer.location=self.cleaned_data.get('Местоположение')
        customer.save()
        
        return user
          
        

class DriverSignUpForm(UserCreationForm):
    Имя = forms.CharField(required=True)
    Фамилия = forms.CharField(required=True)
    Номер_телефона = forms.CharField(required=True)
    Местоположение = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_driver = True
        user.is_staff = True
        user.first_name = self.cleaned_data.get('Имя')
        user.last_name = self.cleaned_data.get('Фамилия')
        user.save()
        group = Group.objects.get(name='drivers')
        user.groups.add(group)
        user.save()
        driver = Driver.objects.create(user=user)
        driver.phone_number=self.cleaned_data.get('Номер_телефона')
        driver.designation=self.cleaned_data.get('Местоположение')
        driver.save()
        return user