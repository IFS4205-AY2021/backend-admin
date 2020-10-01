from django.shortcuts import render

from .models import User, StayHomeRecord
from .serializers import UserSerializer, RecordSerializer

from rest_framework import viewsets, generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    # authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
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

