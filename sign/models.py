from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from datetime import datetime
from django.db import models


class BaseRegisterForm(UserCreationForm):
    username = forms.CharField(label="Логин")
    email = forms.EmailField(label = "Введите Email")
    first_name = forms.CharField(label = "Ваше имя")
    last_name = forms.CharField(label = "Ваша фамилия")
    password1 = forms.CharField(label="Введите пароль")
    password2 = forms.CharField(label="Подтвердите пароль")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class Appointment(models.Model):

    date = models.DateField(

        default=datetime.utcnow,
    )
    client_name = models.CharField(
        max_length=200
    )
    message = models.TextField()

    def __str__(self):
        return f'{self.client_name}: {self.message}'