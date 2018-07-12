from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models
from django.db.models import QuerySet

from assessment.models import ScaleAnswer, Season


class Unit(models.Model):
    name = models.CharField(verbose_name='نام واحد', max_length=30, null=False)

    def __str__(self):
        return self.name


class Job(models.Model):
    pass


class Admin(Job):
    pass


class Employee(Job):
    units = models.ManyToManyField(Unit, verbose_name='واحدها')

    def get_assesseds(self):
        return self.assessments_as_assessor.filter()  # TODO should not show all, should show not considered ones

    def get_user(self):
        return User.objects.filter(job_id=self.pk).first()

    def get_unresolved_answers(self):
        return ScaleAnswer.objects.filter(carried_on=False, assessment__assessor__user=self.get_user())

    def get_units(self):
        return list(self.units.all())

    def get_units_as_string(self):
        names = [unit.name for unit in self.units.all()]
        return '، '.join(names)

    def set_units(self, units):
        self.units.add(*units)

    def get_current_assessment(self):
        return self.assessments_as_assessed.filter(season=Season.objects.get_current_season()).first()

    def has_assessment(self):
        assessment = self.get_current_assessment()
        if assessment:
            return True
        return False

    def assessment_done(self):
        assessment = self.assessments_as_assessed.filter(season=Season.objects.get_current_season()).first()
        if assessment:
            return assessment.is_done()
        return False


class UserQuerySet(QuerySet):
    def employees(self):
        emps = Employee.objects.all()
        return self.filter(job__in=emps)


class UserManager(DjangoUserManager):
    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)

    def create_superuser(self, username, email, password, **extra_fields):
        user = super(UserManager, self).create_superuser(username, email, password, **extra_fields)
        admin = Admin.objects.create()
        user.set_job(admin)
        user.save()
        return user

    def get_by_id(self, user_id):
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

    job = models.ForeignKey('Job', verbose_name='نقش', null=True, blank=True, on_delete=models.SET_NULL)

    objects = UserManager()

    def get_name(self):
        if self.first_name or self.last_name:
            return self.first_name + ' ' + self.last_name
        return self.username

    def __str__(self):
        return self.get_name()

    def is_admin(self):
        if not self.job:
            return False
        if hasattr(self.job, 'admin'):
            return True
        return False

    def is_employee(self):
        if not self.job:
            return False
        if hasattr(self.job, 'employee'):
            return True
        return False

    def get_admin(self)-> Admin:
        if self.is_admin():
            return self.job.admin
        return None

    def get_employee(self)-> Employee:
        if self.is_employee():
            return self.job.employee
        return None

    def set_job(self, job):
        self.job = job

    def get_personnel_code(self):
        return self.personnel_code


