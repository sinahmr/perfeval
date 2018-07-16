from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models
from django.db.models import QuerySet
from django.core.exceptions import PermissionDenied
from polymorphic.models import PolymorphicModel

from assessment.models import ScaleAnswer, Season, QuantitativeCriterion, QualitativeCriterion, Assessment, \
    PunishmentReward

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


class Job(PolymorphicModel):
    permissions = models.ManyToManyField(Permission)

    def get_id(self):
        return self.id

    def get_user(self):
        return self.user.first()

    def get_name(self):
        return self.get_user().get_name()

    def set_permissions(self):
        pass

    def get_permissions(self):
        return self.permissions.all()

    def show_employee_page(self, employee, context):
        pass

    def _employee_details(self, employee, context):
        not_found_user = False
        user = employee.get_user()
        punishment_reward = None
        assessment = employee.get_current_assessment_assessed()
        if assessment:
            punishment_reward = assessment.get_punishment_reward()
        if not user:
            not_found_user = True
        context['not_found_user'] = not_found_user
        context['user'] = user
        context['employee'] = employee
        context['is_admin'] = self.is_admin()
        context['assessment'] = assessment
        context['punishment_reward'] = punishment_reward
        return context

    def is_admin(self):
        pass

    def is_employee(self):
        pass

    def __str__(self):
        return self.get_user().get_name()


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

    def show_employee_page(self, user, context):
        if self.get_user() != user:
            return self._employee_details(user, context)
        raise PermissionDenied("access denied")

    def is_admin(self):
        return True

    def is_employee(self):
        return False

    def add_employee(self, units):
        employee = Employee.objects.create()
        employee.set_units(units)
        employee.save()
        return employee

    def add_scale(self, scale, quan, qual, quan_interpretation, qual_interpretation):
        if qual:
            qual = QualitativeCriterion.objects.create(choices=qual, interpretation=qual_interpretation)
            scale.set_qualitative_criterion(qual)
        if quan:
            quan = QuantitativeCriterion.objects.create(formula=quan, interpretation=quan_interpretation)
            scale.set_quantitative_criterion(quan)
        return scale


class Employee(Job):
    units = models.ManyToManyField(Unit, verbose_name='واحدها')

    def get_assesseds(self):
        return self.assessments_as_assessor.filter()  # TODO should not show all, should show not considered ones

    def get_assessor(self):
        assessmnet = self.assessments_as_assessed.first()
        if assessmnet:
            return assessmnet.get_assessor()
        return None

    def get_unresolved_answers(self):
        return ScaleAnswer.objects.filter(carried_on=False, assessment__assessor__user=self.get_user())

    def get_units(self):
        return list(self.units.all())

    def get_units_as_string(self):
        names = [unit.name for unit in self.units.all()]
        return '، '.join(names)

    def set_units(self, units):
        self.units.add(*units)

    def get_current_assessment_assessed(self):
        return self.assessments_as_assessed.filter(season=Season.objects.get_current_season()).first()

    def get_current_assessment_assessor(self):
        return self.assessments_as_assessor.filter(season=Season.objects.get_current_season()).first()

    def has_assessor(self):
        assessment = self.get_current_assessment_assessed()
        if assessment:
            return True
        return False

    def get_current_assessor(self):
        if self.has_assessor():
            return self.get_current_assessment_assessed().get_assessor()
        return None

    def assessment_done(self):
        assessment = self.assessments_as_assessed.filter(season=Season.objects.get_current_season()).first()
        if assessment:
            return assessment.is_done()
        return False

    def set_permissions(self):
        self.permissions.add(Permission.objects.get(action="E", object="A"))
        self.permissions.add(Permission.objects.get(action="R", object="A"))
        self.save()

    def show_employee_page(self, employee, context):
        if self == employee:
            return self._employee_details(employee, context)
        raise PermissionDenied("access denied")

    def is_admin(self):
        return False

    def is_employee(self):
        return True

    def create_assessment(self, assessor, assessed, scales):
        assessment = Assessment.objects.create(assessor=assessor, assessed=assessed)
        for sc in scales:
            ScaleAnswer.objects.create(scale=sc, assessment=assessment)
        PunishmentReward.objects.create(assessment=assessment)
        return assessment


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

    job = models.ForeignKey('Job', related_name="user", related_query_name="user",
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

    def get_job(self):
        return self.job

    def set_job(self, job):
        self.job = job
        self.job.set_permissions()

    def get_personnel_code(self):
        return self.personnel_code

    def has_permission(self, action, obj):
        permission = Permission.objects.get(action=action, object=obj)
        if permission in self.job.get_permissions():
            return True
        raise PermissionDenied("permission denied!")

    def show_employee_page(self, employee, context):
        return self.get_job().show_employee_page(employee, context)
