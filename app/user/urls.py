from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

urlpatterns = [
    path('', UserViewSet.as_view({'get':'list', 'post':'create'}), name='user_view'),
    path('tracer/record/', RecordViewSet.as_view({'get': 'list'}), name='record_view'),
    # path('api-token/', TokenObtainPairView.as_view()),
    # path('api-token-refresh/', TokenRefreshView.as_view()),
    path('tracer/', home, name="tracer_home"),
    path('tracer/search-status/', search_status, name="search_status"),
    path('tracer/change-status/', change_status, name="change_status"),
    path('tracer/search-contact/', search_contact, name="search_contact"),
    path('tracer/add-contact/', add_contact, name="add_contact"),
    path('tracer/delete-contact/', delete_contact, name="delete_contact"),
    path('tracer/search-records/', search_records, name="search_records"),
    path('tracer/contact-graph/', generate_graph, name="generate_graph"),
    path('tracer/initiate-cluster/', initiate_cluster, name="initiate_cluster"),

    path('dashboard/', dashboardPage, name='homepage'),
    path('user_page/', userPage, name='user_page'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('register/', registerPage, name='register'),
    path('create_record/', createRecord, name='create_record'),
    path('create_contact/', createContactRecord, name='create_contact'),
    path('update_info/<str:pk>/', updateInfo, name='update_info'),
    path('delete_record/<str:pk>/', deleteRecord, name='delete_record'),
    path('delete_contact/<str:pk>/', deleteContactRecord, name='delete_contact'),
    path('create_stayhomerecord/<str:pk>/', createStayHomeRecord, name='create_stayhomerecord'),
    path('create_stayhomerecord_admin/', createStayHomeRecordAdmin, name='create_stayhomerecord_admin'),
    path('view_stayhomerecord/<str:pk>/', viewStayHomeRecord, name='view_stayhomerecord'),
    path('media/images/<str:img>/', userImage, name='user_image'),

    path('researcher/message_display_home/', message_display_home, name="message_display_home"),
    path('researcher/message_display_dashboard/', message_display_dashboard, name="message_display_dashboard"),
    path('researcher/dashboard/', researcher_dashboard, name="researcher_dashboard"),
    path('researcher/list/', list_, name="list"),
    path('researcher/count_avg/', count_avg, name="count_avg"),
    path('researcher/count_total/', count_total, name="count_total"),
    path('researcher/list_all/', list_all, name="list_all"),
    path('researcher/cluster/', list_clu, name="list_cluster"),
    path('researcher/count_total_P/', count_total_P, name="list_total_POSITIVE"),
    path('researcher/count_avg_P/', count_avg_P, name="list_avg_POSITIVE"),

]



# from rest_framework import routers

# rt = routers.DefaultRouter()
# rt.register(r'user', UserViewSet)
# rt.register(r'record', RecordViewSet)