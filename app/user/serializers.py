from rest_framework import serializers

from .models import User, Admin, StayHomeRecord

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'phone', 'age', 'address', 'location', 'test_result', 'encryption_keys']

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = StayHomeRecord
        fields = '__all__'
