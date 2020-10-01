from django.urls import path
from .views import UserViewSet, RecordViewSet
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

urlpatterns = [
    path('', UserViewSet.as_view({'get': 'list'}), name='user_view'),
    path('record/', RecordViewSet.as_view({'get': 'list'}), name='record_view'),
    path('api-token/', TokenObtainPairView.as_view()),
    path('api-token-refresh/', TokenRefreshView.as_view()),
]



# from rest_framework import routers

# rt = routers.DefaultRouter()
# rt.register(r'user', UserViewSet)
# rt.register(r'record', RecordViewSet)