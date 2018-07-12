from django.db import models


class Season(models.Model):
    title = models.CharField(verbose_name='عنوان', max_length=100, null=False, blank=False)


class QualitativeCriterion(models.Model):
    choices = models.CharField(verbose_name='انتخاب‌ها', max_length=200, null=False, blank=False)
    interpretation = models.TextField()

    def get_choices_list(self):
        if not self.choices or len(self.choices) < 1:
            return []
        return self.choices.split('\n')


class QuantitativeCriterion(models.Model):
    formula = models.CharField(verbose_name='فرمول', max_length=20, null=False, blank=False)
    interpretation = models.TextField()


class Scale(models.Model):
    title = models.CharField(verbose_name='عنوان', max_length=20, null=False)
    description = models.TextField()
    qualitativeCriterion = models.ForeignKey('QualitativeCriterion', on_delete=models.SET_NULL, null=True)
    quantitativeCriterion = models.ForeignKey('QuantitativeCriterion', on_delete=models.SET_NULL, null=True)

    def get_title(self):
        return self.title

    def __str__(self):
        return self.get_title()

    def set_qual_criterion(self, qual):
        self.qualitativeCriterion = qual

    def set_quan_criterion(self, quan):
        self.quantitativeCriterion = quan


class Assessment(models.Model):
    assessor = models.ForeignKey('authentication.Employee', on_delete=models.CASCADE,
                                 related_name="assessments_as_assessor",
                                 related_query_name="assessments_as_assessor",
                                 null=False, blank=False)
    assessed = models.ForeignKey('authentication.Employee', on_delete=models.CASCADE,
                                 related_name="assessments_as_assessed",
                                 related_query_name="assessments_as_assessed",
                                 null=False, blank=False)
    #scales = models.ManyToManyField('Scale',
                                   # verbose_name='معیارها')  # TODO delete, create every ScaleAnswer object when assessment is created
    season = models.ForeignKey('Season', on_delete=models.CASCADE, related_name="assessments",
                               related_query_name="assessments", null=False, blank=False)

    unique_together = ("assessor", "assessed", "season")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_season()


    def set_season(self):
        self.season = Season.objects.last()

    def set_assessor(self, employee):
        self.assessor = employee

    def set_assessed(self, employee):
        self.assessed = employee

    def is_done(self):
        scale_answers = self.scale_answers.all()
        for sc_a in scale_answers:
            if sc_a.is_carried_on() is False:
                return False
        return True


class ScaleAnswer(models.Model):
    carried_on = models.BooleanField(default=False)
    assessment = models.ForeignKey('Assessment', on_delete=models.CASCADE, related_name="scale_answers",
                                   related_query_name="scale_answers")
    scale = models.ForeignKey('Scale', on_delete=models.CASCADE, null=False)
    qualitativeAnswer = models.CharField(max_length=100, null=True, blank=True)
    quantitativeAnswer = models.CharField(max_length=100, null=True, blank=True)

    def is_carried_on(self):
        return self.carried_on


class PunishmentReward(models.Model):
    method = models.TextField(null=False, blank=False)
    type = models.NullBooleanField(null=True)
    season = models.ForeignKey('Season', on_delete=models.CASCADE, related_name="punishment_rewards",
                               related_query_name="punishment_rewards", null=False,
                               blank=False)
    employee = models.ForeignKey('authentication.Employee', on_delete=models.CASCADE)


