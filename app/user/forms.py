from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import *


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class RecordForm(ModelForm):
    class Meta:
        model = Record
        fields = '__all__'

class UserInfoForm(ModelForm):
    class Meta:
        model = UserInfo
        fields = '__all__'