from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import IntegrityError
from django.db import models
from django.db.models import QuerySet
from django.http import Http404

from assessment.models import ScaleAnswer, Season

ACTION_CHOICES = (
    ('C', 'create'),
    ('E', 'edit'),
    ('R', 'read'),
)
OBJECT_CHOICES = (
    ('A', 'Assessment'),
    ('E', 'Employee'),
    ('P', 'PunishmentReward'),
    ('S', 'Scale'),
    ('U', 'Unit'),
    ('N', 'Season')
)


class Permission(models.Model):

    action = models.CharField(choices=ACTION_CHOICES, max_length=50)
    object = models.CharField(choices=OBJECT_CHOICES, max_length=60)




class Unit(models.Model):
    name = models.CharField(verbose_name='نام واحد', max_length=30, null=False)

    def __str__(self):
        return self.name


class Job(models.Model):

    permissions = models.ManyToManyField(Permission)


    def get_id(self):
        return self.id

    def get_user(self):
        return self.user.first()

    def set_permissions(self):
        pass

    def get_permissions(self):
        return self.permissions.all()

    def show_employee_page(self,user, context):
        pass

    def _employee_details(self, user, context):
        not_found_user = False
        assessment = None
        employee = None
        if user:
            employee = user.get_employee()
            if employee:
                assessment = employee.get_current_assessment()
        else:
            not_found_user = True

        context['not_found_user'] = not_found_user
        context['user'] = user
        context['employee'] = employee
        context['viewer'] = self.get_user()
        context['assessment'] = assessment
        return context

class Admin(Job):

    def set_permissions(self):
        self.permissions.add(Permission.objects.get(action="C", object="A"))
        self.permissions.add(Permission.objects.get(action="C", object="S"))
        self.permissions.add(Permission.objects.get(action="C", object="N"))
        self.permissions.add(Permission.objects.get(action="C", object="U"))
        self.permissions.add(Permission.objects.get(action="C", object="E"))
        self.permissions.add(Permission.objects.get(action="R", object="E"))
        self.permissions.add(Permission.objects.get(action="E", object="E"))
        self.permissions.add(Permission.objects.get(action="E", object="P"))
        self.save()

    def show_employee_page(self,user, context):
        if self.get_user() != user:
            return self._employee_details(user, context)
        raise Http404("access denied")



class Employee(Job):

    units = models.ManyToManyField(Unit, verbose_name='واحدها')


    def get_assesseds(self):
        return self.assessments_as_assessor.filter()  # TODO should not show all, should show not considered ones

    def get_assessor(self):
        return self.assessments_as_assessed.first().get_assessor()

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

    def set_permissions(self):
        self.permissions.add(Permission.objects.get(action="E", object="A"))
        self.permissions.add(Permission.objects.get(action="R", object="A"))
        self.save()

    def show_employee_page(self,user, context):
        if self.get_user() == user:
            return self._employee_details(user, context)
        raise Http404("access denied")

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

    job = models.ForeignKey('Job',related_name="user" ,related_query_name="user",
                            verbose_name='نقش', null=True, blank=True, on_delete=models.SET_NULL)

    objects = UserManager()


    def set_permission(self):
        self.job.set_permission()

    def get_username(self):
        return self.username

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_year_of_birth(self):
        return self.year_of_birth

    def get_id(self):
        return self.id

    def get_name(self):
        if self.first_name or self.last_name:
            return self.first_name + ' ' + self.last_name
        return self.username

    def __str__(self):
        return self.get_name()


#################################################TODO
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
###################################################33
    def set_job(self, job):
        self.job = job
        self.job.set_permissions()


    def get_personnel_code(self):
        return self.personnel_code

    def has_permission(self, action, obj):
        permission = Permission.objects.get(action=action, object=obj)
        if permission in self.job.get_permissions():
                return True
        raise Http404("permission denied!")

    def show_employee_page(self,user , context):
        return self.job.show_employee_page(user, context)





