from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

urlpatterns = [
    path('api-token/', TokenObtainPairView.as_view()),
    path('api-token-refresh/', TokenRefreshView.as_view()),
]



# from rest_framework import routers

# rt = routers.DefaultRouter()
# rt.register(r'user', UserViewSet)
# rt.register(r'record', RecordViewSet)