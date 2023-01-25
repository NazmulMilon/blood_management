from django.shortcuts import render
from .models import UserProfile
from .serializers import UserProfileCreateSerializer, UserProfileListSerializer, UserListSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView
# Create your views here.


class UserProfileCreateAPIView(CreateAPIView):
    serializer_class = UserProfileCreateSerializer
    queryset = UserProfile.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.data
        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)
        username = data.get('username', None)
        email = data.get('email', None)
        password = data.get('password', None)
        phone_no = data.get('phone_no', None)
        blood_group = data.get('blood_group', None)
        user_type = data.get('user_type', None)
        last_donation_date = data.get('last_donation_date', None)
        date_of_birth = data.get('date_of_birth', None)
        donation_area = data.get('donation_area', None)
        permanent_address = data.get('permanent_address', None)
        gender = data.get('gender', None)

        if User.objects.filter(username=username).exists():
            return Response(data={'details': 'User already Exists'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
        user.save()

        user_profile = UserProfile(user=user, phone_no=phone_no, blood_group=blood_group, user_type=user_type,
                                   last_donation_date=last_donation_date, date_of_birth=date_of_birth,
                                   donation_area=donation_area, permanent_address=permanent_address, gender=gender)
        user_profile.save()
        return Response(data={'details': 'New User Profile Created'}, status=status.HTTP_201_CREATED)


class UserProfileListAPIView(ListAPIView):
    serializer_class = UserProfileListSerializer
    queryset = UserProfile.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = UserProfile.objects.all()
        serializer = UserProfileListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserListAPIView(ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = User.objects.all()
        serializer = UserListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)