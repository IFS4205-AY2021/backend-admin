from rest_framework import serializers

from .models import UserInfo, Admin, StayHomeRecord

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = '__all__'

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = StayHomeRecord
        fields = '__all__'
