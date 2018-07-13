from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db import models


class SeasonManager(DjangoUserManager):
    def get_current_season(self):
        return self.last()


class Season(models.Model):
    title = models.CharField(verbose_name='عنوان', max_length=100, null=False, blank=False)

    objects = SeasonManager()

    def get_title(self):
        return self.title

    def get_id(self):
        return self.id


class QualitativeCriterion(models.Model):
    choices = models.CharField(verbose_name='انتخاب‌ها', max_length=200, null=False, blank=False)
    interpretation = models.TextField()

    def get_choices_list(self):
        if not self.choices or len(self.choices) < 1:
            return []
        return self.choices.split('\n')

    def get_interpretation(self):
        return self.interpretation

    def get_id(self):
        return self.id


class QuantitativeCriterion(models.Model):
    formula = models.CharField(verbose_name='فرمول', max_length=20, null=False, blank=False)
    interpretation = models.TextField()

    def get_formula(self):
        return self.formula

    def get_interpretation(self):
        return self.interpretation

    def get_id(self):
        return self.id


class Scale(models.Model):
    title = models.CharField(verbose_name='عنوان', max_length=20, null=False)
    description = models.TextField()
    qualitativeCriterion = models.ForeignKey('QualitativeCriterion', on_delete=models.SET_NULL, null=True)
    quantitativeCriterion = models.ForeignKey('QuantitativeCriterion', on_delete=models.SET_NULL, null=True)

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def __str__(self):
        return self.get_title()

    def set_qualitative_criterion(self, qual):
        self.qualitativeCriterion = qual

    def set_quantitative_criterion(self, quan):
        self.quantitativeCriterion = quan

    def get_qualitative_criterion(self):
        return self.qualitativeCriterion

    def get_quantitative_criterion(self):
        return self.quantitativeCriterion

    def get_id(self):
        return self.id


class Assessment(models.Model):
    assessor = models.ForeignKey('authentication.Employee', on_delete=models.CASCADE,
                                 related_name="assessments_as_assessor",
                                 related_query_name="assessments_as_assessor",
                                 null=False, blank=False)
    assessed = models.ForeignKey('authentication.Employee', on_delete=models.CASCADE,
                                 related_name="assessments_as_assessed",
                                 related_query_name="assessments_as_assessed",
                                 null=False, blank=False)
    season = models.ForeignKey('Season', on_delete=models.CASCADE, related_name="assessments",
                               related_query_name="assessments", null=False, blank=False)

    unique_together = ('assessed', 'season')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_season()

    def get_punishment_reward(self):
        return self.punishmentreward

    def set_season(self):
        self.season = Season.objects.get_current_season()

    def get_season(self):
        return self.season

    def set_assessor(self, employee):
        self.assessor = employee

    def set_assessed(self, employee):
        self.assessed = employee

    def get_assessor(self):
        return self.assessor

    def get_assessed(self):
        return self.assessed

    def get_scale_answers(self):
        return self.scale_answers.all()

    def is_done(self):
        scale_answers = self.scale_answers.all()
        for sc_a in scale_answers:
            if sc_a.is_carried_on() is False:
                return False
        return True

    def get_id(self):
        return self.id


class ScaleAnswer(models.Model):
    carried_on = models.BooleanField(verbose_name='انجام‌شده', default=False)
    assessment = models.ForeignKey('Assessment', on_delete=models.CASCADE, related_name="scale_answers",
                                   related_query_name="scale_answers")
    scale = models.ForeignKey('Scale', on_delete=models.CASCADE, null=False)
    qualitativeAnswer = models.CharField(verbose_name='پاسخ کیفی', max_length=100, null=True, blank=True)
    quantitativeAnswer = models.CharField(verbose_name='پاسخ کمی', max_length=100, null=True, blank=True)

    def set_carried_on(self, carried_on):
        self.carried_on = carried_on

    def is_carried_on(self):
        return self.carried_on

    def get_id(self):
        return self.id

    def get_assessment(self):
        return self.assessment

    def get_scale(self):
        return self.scale

    def get_qualitative_answer(self):
        return self.qualitativeAnswer

    def get_quantitative_answer(self):
        return self.quantitativeAnswer

    def set_qualitative_answer(self, qual):
        self.qualitativeAnswer = qual

    def set_quantitative_answer(self, quan):
        self.quantitativeAnswer = quan


class PunishmentReward(models.Model):
    TYPE_CHOICES = (
        ('R', 'تشویق'),
        ('P', 'تنبیه'),
        ('N', 'نه تشویق و نه تنبیه')
    )

    type = models.CharField(verbose_name='نوع', max_length=1, choices=TYPE_CHOICES, default='N')
    method = models.TextField(verbose_name='روش', null=True, blank=True)
    assessment = models.OneToOneField('Assessment', on_delete=models.CASCADE)

    def get_id(self):
        return self.id

    def get_type(self):
        return self.type

    def get_method(self):
        return self.method

    def get_assessment(self):
        return self.assessment
