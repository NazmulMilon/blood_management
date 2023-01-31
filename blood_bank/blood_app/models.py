
from django.db import models
from systems.models import BaseModel
from systems.enums import BloodGroupType, UserRole, GenderType, StorageType
from django.contrib.auth.models import User


# Create your models here.

class UserProfile(BaseModel):
    user = models.ForeignKey(User, models.CASCADE, help_text="donor's user name")
    phone_no = models.IntegerField(help_text="donor's mobile number")
    blood_group = models.CharField(max_length=10, choices=BloodGroupType.choices(),
                                   default=BloodGroupType.B_POSITIVE.value)
    user_type = models.CharField(max_length=50, choices=UserRole.choices(), default=UserRole.DONOR.value)
    last_donation_date = models.DateField(auto_now_add=False)
    date_of_birth = models.DateField(auto_now_add=False)
    donation_area = models.CharField(max_length=100, help_text="donor's donation area")
    permanent_address = models.CharField(max_length=100, help_text="donor's permanent address")
    gender = models.CharField(max_length=10, choices=GenderType.choices(), default=GenderType.MALE.value)

    class Meta:
        db_table = 'user_profiles'


class Storage(BaseModel):
    blood_group = models.CharField(max_length=10, choices=BloodGroupType.choices(),
                                   default=BloodGroupType.B_POSITIVE.value)
    whole_blood = models.IntegerField(blank=True)
    frozen_plasma = models.IntegerField(blank=True)
    platelet = models.IntegerField(blank=True)
    storage_type = models.CharField(max_length=20, choices=StorageType.choices(), default=StorageType.STORAGE_INCREASE.value)

    class Meta:
        db_table = 'storage'

