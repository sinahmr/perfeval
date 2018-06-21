from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import IntegrityError
from django.db import models

from .exceptions import RepetitiousUsername


class Unit(models.Model):
    name = models.CharField(verbose_name='نام واحد', max_length=30, null=False)

    def __str__(self):
        return self.name


class UserManager(DjangoUserManager):
    def create_superuser(self, username, email, password, **extra_fields):
        user = super(UserManager, self).create_superuser(username, email, password, **extra_fields)
        Admin.objects.create(user_ptr=user)
        user.save()
        return user

    def get_by_username(self, username):  # TODO not used
        try:
            return self.get(username=username)
        except User.DoesNotExist:
            return None

    def get_by_id(self, user_id):  # TODO not used
        try:
            return self.get(pk=user_id)
        except User.DoesNotExist:
            return None


class User(AbstractUser):
    first_name = models.CharField(verbose_name='نام', max_length=30)
    last_name = models.CharField(verbose_name='نام خانوادگی', max_length=150)
    father_name = models.CharField(verbose_name='نام پدر', max_length=30, null=True, blank=True)
    personnel_code = models.CharField(verbose_name='شماره پرسنلی', max_length=8, null=False, unique=True)
    national_code = models.CharField(verbose_name='کد ملی', max_length=10, null=False, unique=True)
    year_of_birth = models.IntegerField(verbose_name='سال تولد', null=True, blank=True)
    mobile = models.CharField(verbose_name='موبایل', max_length=15, null=True)

    objects = UserManager()

    def get_name(self):
        if self.first_name or self.last_name:
            return self.first_name + ' ' + self.last_name
        return self.username

    def __str__(self):
        return self.get_name()

    def is_admin(self):
        if hasattr(self, 'admin'):
            return True
        return False

    def is_employee(self):
        if hasattr(self, 'employee'):
            return True
        return False

    def change_username_and_password(self, new_username, new_password):  # TODO not used
        self.username = new_username
        self.set_password(new_password)
        try:
            self.save()
        except IntegrityError:
            raise RepetitiousUsername()


class Admin(User):
    pass


class Employee(User):
    units = models.ManyToManyField(Unit, verbose_name='واحدها')

    @property
    def get_assesseds(self):
        assessments = self.assessments_as_assessor.all()
        assesseds = []
        for assessment in assessments:
            assesseds.append(assessment.assessed)
        return assesseds
