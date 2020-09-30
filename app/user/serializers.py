from rest_framework import serializers

from .models import User, StayHomeRecord, Admin

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'phone', 'age', 'address', 'location', 'test_result', 'encryption_keys']

