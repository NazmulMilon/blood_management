from django.shortcuts import render
from .models import UserProfile, Storage
from .serializers import UserProfileCreateSerializer, UserProfileListSerializer, UserListSerializer, \
    UserProfileRetrieveSerializer, UserRetrieveSerializer, DonorSearchSerializer, StorageListSerializer, \
    StorageRetrieveSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView
from django.db import transaction
from django.db.models import Q
from rest_framework.validators import ValidationError
# Create your views here.


class UserProfileCreateAPIView(CreateAPIView):
    serializer_class = UserProfileCreateSerializer

    @transaction.atomic
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


class UserProfileRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserProfileRetrieveSerializer
    queryset = UserProfile.objects.all()

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        profile_obj = UserProfile.objects.filter(pk=pk).first()
        serializer = UserProfileRetrieveSerializer(profile_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserListAPIView(ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = User.objects.all()
        serializer = UserListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserRetrieveSerializer
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user_obj = User.objects.filter(pk=pk).first()
        serializer = UserRetrieveSerializer(user_obj)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserProfileSearchAPIView(RetrieveAPIView):
    serializer_class = DonorSearchSerializer
    queryset = UserProfile.objects.all()

    def get(self, request, *args, **kwargs):
        value = kwargs.get('value', None)
        queryset = UserProfile.objects.filter(Q(blood_group=value) | Q(donation_area=value))
        serializer = DonorSearchSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


# class UserProfileSearchAPIView(RetrieveAPIView):
#     serializer_class = DonorSearchSerializer
#     queryset = UserProfile.objects.all()
#
#     def get(self, request, *args, **kwargs):
#         value1 = request.data.get('donation_area', None)
#         value2 = request.data.get('blood_group', None)
#         queryset = UserProfile.objects.filter(blood_group=value2) or UserProfile.objects.filter(donation_area=value1)
#         serializer = DonorSearchSerializer(queryset, many=True)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)
#

# class UserProfileSearchAPIView(RetrieveAPIView):
#     serializer_class = DonorSearchSerializer
#     queryset = UserProfile.objects.all()

    # def get(self, request, *args, **kwargs):
    #     obj = None
    #     value = kwargs.get('value', None)
    #     # value2 = request.data.get('blood_group', None)
    #
    #     if UserProfile.objects.filter(phone_no=value).exists():
    #         obj = UserProfile.objects.filter(phone_no=value)
    #     elif UserProfile.objects.filter(donation_area=value).exists():
    #         obj = UserProfile.objects.filter(donation_area=value)
    #     elif UserProfile.objects.filter(blood_group=value).exists():
    #         obj = UserProfile.objects.filter(blood_group=value)
    #     else:
    #         return Response(data={'details': 'Donor not found.'}, status=status.HTTP_204_NO_CONTENT)
    #
    #     serializer = DonorSearchSerializer(obj, many=True)
    #     return Response(data=serializer.data, status=status.HTTP_200_OK)
    #


class StorageListAPIView(ListAPIView):
    queryset = Storage.objects.all()
    serializer_class = StorageListSerializer

    def get(self, request, *args, **kwargs):
        queryset = Storage.objects.all().order_by('blood_group')
        serializer = StorageListSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class StorageRetrieveAPIView(RetrieveAPIView):
    serializer_class = StorageRetrieveSerializer
    queryset = Storage.objects.all()

    def get(self, request, *args, **kwargs):
        value = kwargs.get('value', None)
        storage_obj = Storage.objects.filter(blood_group=value).first()
        serializer = self.serializer_class(storage_obj)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class StorageDecreaseAPIView(UpdateAPIView):
    serializer_class = StorageRetrieveSerializer
    queryset = Storage.objects.all()

    def put(self, request, *args, **kwargs):
        value = kwargs.get('value', None)
        storage_obj = Storage.objects.filter(blood_group=value).first()
        data = request.data
        storage_type = data.get('storage_type')
        whole_blood = data.get('whole_blood', None)
        frozen_plasma = data.get('frozen_plasma', None)
        platelet = data.get('platelet', None)

        if storage_type == "TAKE":
            if whole_blood is not None:
                if storage_obj.whole_blood >= whole_blood:
                    storage_obj.whole_blood -= whole_blood
                    storage_obj.save()
            if frozen_plasma is not None:
                if storage_obj.frozen_plasma >= frozen_plasma:
                    storage_obj.frozen_plasma -= frozen_plasma
                    storage_obj.save()
            if platelet is not None:
                if storage_obj.platelet >= platelet:
                    storage_obj.platelet -= platelet
                    storage_obj.save()
        elif storage_type == "DONATE":
            if whole_blood is not None:
                if storage_obj.whole_blood >= 0:
                    storage_obj.whole_blood += whole_blood
                    storage_obj.save()
            if frozen_plasma is not None:
                if storage_obj.frozen_plasma >= 0:
                    storage_obj.frozen_plasma += frozen_plasma
                    storage_obj.save()
            if platelet is not None:
                if storage_obj.platelet >= 0:
                    storage_obj.platelet += platelet
                    storage_obj.save()
        serializer = StorageRetrieveSerializer(storage_obj)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class StorageCreateAPIView(CreateAPIView):
    serializer_class = StorageRetrieveSerializer
    queryset = Storage.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.data
        blood_group = data.get('blood_group', None)
        if blood_group is None:
            raise ValidationError
        if Storage.objects.filter(blood_group=blood_group).exists():
            return Response(data={'details': 'Blood Group is already exists.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        whole_blood = data.get('whole_blood', None)
        frozen_plasma = data.get('frozen_plasma', None)
        platelet = data.get('platelet', None)

        blood_obj = Storage(blood_group=blood_group, whole_blood=whole_blood, frozen_plasma=frozen_plasma,
                            platelet=platelet)
        blood_obj.save()
        serializer = self.serializer_class(blood_obj)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


