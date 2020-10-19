from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

urlpatterns = [
    path('', UserViewSet.as_view({'get':'list', 'post':'create'}), name='user_view'),
    path('record/', RecordViewSet.as_view({'get': 'list'}), name='record_view'),
    # path('api-token/', TokenObtainPairView.as_view()),
    # path('api-token-refresh/', TokenRefreshView.as_view()),
    path('dashboard/', dashboardPage, name='home'),
    path('user_page/', userPage, name='user_page'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('register/', registerPage, name='register'),
    path('create_record/', createRecord, name='create_record'),
    path('update_info/<str:pk>/', updateInfo, name='update_info'),
    path('delete_record/<str:pk>/', deleteRecord, name='delete_record'),
    path('create_stayhomerecord/<str:pk>/', createStayHomeRecord, name='create_stayhomerecord'),
    path('view_stayhomerecord/<str:pk>/', viewStayHomeRecord, name='view_stayhomerecord'),
    path('media/images/<str:img>/', userImage, name='user_image')
]



# from rest_framework import routers

# rt = routers.DefaultRouter()
# rt.register(r'user', UserViewSet)
# rt.register(r'record', RecordViewSet)