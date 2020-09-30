from django.contrib import admin
from .models import User, StayHomeRecord, Admin
# Register your models here.
admin.site.register(User)
admin.site.register(StayHomeRecord)
admin.site.register(Admin)
