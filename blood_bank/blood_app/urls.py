from django.urls import path
from .views import UserProfileCreateAPIView, UserProfileListAPIView, UserListAPIView, UserProfileRetrieveAPIView, \
    UserRetrieveAPIView, UserProfileSearchAPIView
urlpatterns = [
    path('profile/create/', UserProfileCreateAPIView.as_view(), name='user_create'),
    path('profile/list/all/', UserProfileListAPIView.as_view(), name='user_create'),
    path('list/all/', UserListAPIView.as_view(), name='user_create'),
    path('profile/<int:pk>/', UserProfileRetrieveAPIView.as_view(), name='user_profile_retrieve'),
    # path('donor/<str:value>/', UserProfileSearchAPIView.as_view(), name='user_profile_search'),
    path('donor/search/', UserProfileSearchAPIView.as_view(), name='user_profile_search'),


    path('user/retrieve/<int:pk>/', UserRetrieveAPIView.as_view(), name='user_retrieve'),
]
