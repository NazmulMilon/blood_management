from enum import Enum


class BaseEnum(Enum):
    """
     Let's allow using an Enum class in model Field choices and make code more simple and modular.
     Ref: https://code.djangoproject.com/ticket/27910
     Ref: https://stackoverflow.com/questions/54802616/how-to-use-enums-as-a-choice-field-in-django-model
    """

    def __init__(self, *args):
        cls = self.__class__
        if any(self.value == e.value for e in cls):
            a = self.name
            e = cls(self.value).name

            raise ValueError("aliases not allowed in DuplicateFreeEnum:  %r --> %r" % (a, e))

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class BloodGroupType(BaseEnum):
    B_POSITIVE = 'B+'
    A_POSITIVE = 'A+'
    O_POSITIVE = 'O+'
    AB_POSITIVE = 'AB+'
    B_NEGATIVE = 'B-'
    A_NEGATIVE = 'A-'
    O_NEGATIVE = 'O-'
    AB_NEGATIVE = 'AB-'


class UserRole(BaseEnum):
    DONOR = 'DONOR'
    RECIPIENT = 'RECIPIENT'
    STAFF = 'STAFF'


class GenderType(BaseEnum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'


class StorageType(BaseEnum):
    STORAGE_INCREASE = "DONATE"
    STORAGE_TAKE = "TAKE"
