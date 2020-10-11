from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import UserInfo

# def userInfo(sender, instance, created, **kwargs):
#     if created:
#         group = Group.objects.get(name='normal_user')
#         instance.groups.add(group)
#         print(instance)
#         UserInfo.objects.create(relate=instance, name=instance.username,)
#         print('UserInfo created.')

# post_save.connect(userInfo, sender=User)