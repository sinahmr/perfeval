from django.db import models
from django.db import IntegrityError
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from .exceptions import RepetitiousUsername, FailedLogin


class Unit(models.Model):
    name = models.CharField(verbose_name='نام واحد', max_length=30)

    def __str__(self):
        return self.name


# TODO handle down cast for user
# TODO every class should have create method
# TODO apply to class diagram: year_of_birth, personnel_code, first_name, last_name, mobile
class User(AbstractUser):
    father_name = models.CharField(verbose_name='نام پدر', max_length=30)
    personnel_code = models.CharField(verbose_name='شماره پرسنلی', max_length=8)
    national_code = models.CharField(verbose_name='کد ملی', max_length=10)
    year_of_birth = models.IntegerField(verbose_name='سال تولد')
    mobile = models.CharField(verbose_name='موبایل', max_length=15)

    @classmethod
    def create(cls, **kwargs):
        user = User(**kwargs)
        user.set_password(kwargs.get('password'))
        user.save()
        return user

    @classmethod
    def login(cls, request, username, password):
        user = authenticate(username=username, password=password)
        if not user:
            raise FailedLogin
        auth_login(request, user)
        return user

    @classmethod
    def logout(cls, request):
        auth_logout(request)

    @classmethod
    def get_user_by_username(cls, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    @classmethod
    def get_user_by_id(cls, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def get_name(self):
        if self.first_name or self.last_name:
            return self.first_name + ' ' + self.last_name
        return self.username

    def __str__(self):
        return self.get_name()

    def change_username_and_password(self, new_username, new_password):
        self.username = new_username
        self.set_password(new_password)
        try:
            self.save()
        except IntegrityError:
            raise RepetitiousUsername()


class GeneralAdmin(User):
    @classmethod
    def create(cls, **kwargs):
        ga = GeneralAdmin(**kwargs)
        ga.set_password(kwargs.get('password'))
        ga.save()
        return ga

    @staticmethod
    def add_user(username, password, first_name, last_name, father_name,
                 personnel_code, national_code, year_of_birth, mobile):
        User(username=username, password=password, first_name=first_name, last_name=last_name, father_name=father_name,
             personnel_code=personnel_code, national_code=national_code, year_of_birth=year_of_birth, mobile=mobile)

    @staticmethod
    def delete_user(user):
        user.delete()


class Employee(User):
    @classmethod
    def create(cls, **kwargs):
        e = Employee(**kwargs)
        e.set_password(kwargs.get('password'))
        e.save()
        return e

    unit = models.ForeignKey(Unit, verbose_name='واحد', on_delete=models.CASCADE)


class UnitAdmin(Employee):
    @classmethod
    def create(cls, **kwargs):
        ua = UnitAdmin(**kwargs)
        ua.set_password(kwargs.get('password'))
        ua.save()
        return ua
