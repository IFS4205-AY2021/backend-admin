# backend-admin
Admin subsystem back end.


## TO be added to Dockerfile
```
pip3 install django-cors-headers
pip3 install djangorestframework

python3 manage.py shell

# From Django Shell:

from user.models import User
user1 = User.objects.create(name='James White', phone='93928687', age=32, address='PGPR NUS 118425', location='block 17', test_result=User.TestResult.NEGATIVE, encryption_keys='')
user2 = User.objects.create(name='Jake Lovegood', phone='93927394', age=24, address='PGPR NUS 118425', location='block 31', test_result=User.TestResult.NEGATIVE, encryption_keys='')
user3 = User.objects.create(name='Chris Lee', phone='93920164', age=23, address='PGPR NUS 118425', location='block 28', test_result=User.TestResult.NEGATIVE, encryption_keys='')
```

