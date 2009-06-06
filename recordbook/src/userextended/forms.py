# -*- coding: UTF-8 -*-

from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.forms.util import ErrorList

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
    def clean(self):
        data = self.cleaned_data
        try:
            user = User.objects.get(username = data['username'])
            if not user.check_password(data['password']):
                self._errors['password'] = ErrorList([u'Неправильный пароль'])
                del data['password']
        except ObjectDoesNotExist:
            self._errors['username'] = ErrorList([u'Неправильное имя пользователя'])
            del data['password']
        return data