from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.contrib.auth.models import User
from datetime import datetime, date
# Create your models here.
class UserInfo(models.Model):
    class TestResult(models.TextChoices):
        POSITIVE=True
        NEGATIVE=False
        UNKNOWN=None
    relate          = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name            = models.CharField(max_length=64)
    phone           = models.CharField(max_length=12)
    age             = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(120)])
    location        = models.CharField(max_length=6, validators=[MinLengthValidator(6)])
    address         = models.CharField(max_length=16)
    test_result     = models.CharField(max_length=5, choices=TestResult.choices, default=TestResult.UNKNOWN)
    encryption_keys = models.TextField(blank=True, null=True)
    def __str__(self):
        return str(self.id) + self.name

class StayHomeRecord(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    name            = models.CharField(max_length=64)
    phone           = models.CharField(max_length=12)
    time_uploaded   = models.DateTimeField(default=datetime.now, blank=True)
    location        = models.CharField(max_length=6, validators=[MinLengthValidator(6)])
    address         = models.TextField(blank=True, null=True)
    images          = models.TextField(blank=True, null=True)
    videos          = models.TextField(blank=True, null=True)
    documents       = models.TextField(blank=True, null=True)
    def __str__(self):
        return str(self.user)

class Contact(models.Model):
    user1           = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contact1')
    user2           = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contact2')

class Record(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    date            = models.DateField(default=date.today)
    time            = models.DateTimeField(default=datetime.now)
    location        = models.CharField(max_length=6, validators=[MinLengthValidator(6)])
    address         = models.CharField(max_length=16)
    def __str__(self):
        return str(self.user)

### May not be used, as users are based on Django users
class Admin(models.Model):
    name            = models.CharField(max_length=64)
    phone           = models.CharField(max_length=12)
    encryption_keys = models.TextField(blank=True, null=True)

class Location(models.Model):
    postcode        = models.CharField(max_length=6, validators=[MinLengthValidator(6)])
    name            = models.CharField(max_length=64)

class Researcher(models.Model):
    name            = models.CharField(max_length=64)
    phone           = models.CharField(max_length=12)
    encryption_keys = models.TextField(blank=True, null=True)

class Tracer(models.Model):
    name            = models.CharField(max_length=64)
    phone           = models.CharField(max_length=12)
    encryption_keys = models.TextField(blank=True, null=True)
