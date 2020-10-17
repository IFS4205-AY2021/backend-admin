from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
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
    address         = models.TextField(blank=True, null=True)
    location        = models.CharField(max_length=32)
    test_result     = models.CharField(max_length=5, choices=TestResult.choices)
    encryption_keys = models.TextField(blank=True, null=True)
    def __str__(self):
        return str(self.id) + self.name

class StayHomeRecord(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    name            = models.CharField(max_length=64)
    phone           = models.CharField(max_length=12)
    address         = models.TextField(blank=True, null=True)
    location        = models.CharField(max_length=6)
    images          = models.TextField(blank=True, null=True)
    videos          = models.TextField(blank=True, null=True)
    documents       = models.TextField(blank=True, null=True)
    def __str__(self):
        return str(self.phone)

class Admin(models.Model):
    name            = models.CharField(max_length=64)
    phone           = models.CharField(max_length=12)
    encryption_keys = models.TextField(blank=True, null=True)

class Location(models.Model):
    postcode        = models.CharField(max_length=6)
    name            = models.CharField(max_length=64)

class Researcher(models.Model):
    name            = models.CharField(max_length=64)
    phone           = models.CharField(max_length=12)
    encryption_keys = models.TextField(blank=True, null=True)

class Tracer(models.Model):
    name            = models.CharField(max_length=64)
    phone           = models.CharField(max_length=12)
    encryption_keys = models.TextField(blank=True, null=True)

class Contact(models.Model):
    phone1           = models.CharField(max_length=12)
    phone2           = models.CharField(max_length=12)

class Record(models.Model):
    phone           = models.CharField(max_length=12)
    date            = models.PositiveIntegerField()
    time            = models.PositiveIntegerField()
    location        = models.CharField(max_length=8)
    address         = models.CharField(max_length=16)
    def __str__(self):
        return self.location

