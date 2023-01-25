from django.contrib.auth.models import User
from .models import UserProfile
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField


class UserProfileCreateSerializer(ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=False)
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = UserProfile
        exclude = ['created_at', 'updated_at']


class UserProfileListSerializer(ModelSerializer):
    first_name = SerializerMethodField()

    # last_name = SerializerMethodField()
    # email = SerializerMethodField()
    #
    def get_first_name(self, instance):
        # return instance.user.first_name if instance.user else None
        queryset = User.objects.filter(id=instance.user.id)
        return UserListSerializer(queryset, many=True).data

    class Meta:
        model = UserProfile
        exclude = ['created_at', 'updated_at']


class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        # exclude = ['created_at', 'updated_at']
