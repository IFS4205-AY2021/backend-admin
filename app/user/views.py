from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import Group

from .models import *
from .serializers import UserInfoSerializer, RecordSerializer

from rest_framework import viewsets, generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .decorators import unauthenticated_user, allowed_users, admin_only

class UserViewSet(viewsets.ModelViewSet):
    # authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = UserInfoSerializer(queryset, many=True)
        return Response(serializer.data)
    

class RecordViewSet(viewsets.ModelViewSet):
    # authentication_classes = (BasicAuthentication,)
    # permission_classes = (IsAuthenticated,)
    queryset = StayHomeRecord.objects.all()
    serializer_class = RecordSerializer
    # def get(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = RecordSerializer(queryset, many=True)
    #     return Response(serializer.data)

@login_required(login_url='login')
@admin_only
def dashboardPage(request):

    personalInfo = User.objects.all()
    records = Record.objects.all()
    stayhomerecords = StayHomeRecord.objects.all()
    context = {'info': personalInfo, 'records':records, 'stayhomerecords':stayhomerecords}
    return render(request, 'user/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['normal_user'])
def userPage(request):
    # info  = request.user.relate.objects.all()
    context = {}
    return render(request, 'user/user.html', context)


@unauthenticated_user
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('home')
		# else:
		# 	messages.info(request, 'Username OR password is incorrect')
	context = {}
	return render(request, 'user/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@unauthenticated_user
def registerPage(request):

    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='normal_user')
            UserInfo.objects.create(
                relate=user
            )
            user.groups.add(group)
            return redirect('login')

    context = {'form':form}
    return render(request, 'user/register.html', context)