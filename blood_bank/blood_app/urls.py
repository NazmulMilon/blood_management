from django.urls import path
from .views import UserProfileCreateAPIView, UserProfileListAPIView, UserListAPIView
urlpatterns = [
    path('user/create/', UserProfileCreateAPIView.as_view(), name='user_create'),
    path('user/list/all/', UserProfileListAPIView.as_view(), name='user_create'),
    path('list/all/', UserListAPIView.as_view(), name='user_create'),
]
