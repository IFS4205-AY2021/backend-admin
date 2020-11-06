from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import HiddenInput
from .models import *


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class RecordForm(ModelForm):
    # user = models.ForeignKey(User)
    class Meta:
        model = Record
        fields = ['date', 'time', 'location', 'address']
    # def __init__(self, *args, **kwargs):
    #     self.Meta.fields['user'].widget = HiddenInput()

class StayHomeRecordForm(ModelForm):
    class Meta:
        model = StayHomeRecord
        fields = ['phone', 'time_uploaded', 'location', 'address', 'images', 'videos', 'documents']

class StayHomeRecordForm(ModelForm):
    class Meta:
        model = StayHomeRecord
        fields = [ 'location', 'address', 'images', 'videos', 'documents']

class UserInfoForm(ModelForm):
    class Meta:
        model = UserInfo
        fields = '__all__'

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
