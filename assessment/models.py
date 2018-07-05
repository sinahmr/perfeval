from django.db import models

from authentication.models import Employee


class Season(models.Model):
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()


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
    qualitativeCriterion = models.ForeignKey(QualitativeCriterion, on_delete=models.SET_NULL, null=True)
    quantitativeCriterion = models.ForeignKey(QuantitativeCriterion, on_delete=models.SET_NULL, null=True)


class Assessment(models.Model):
    assessor = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="assessments_as_assessor",
                                 related_query_name="assessments_as_assessor",
                                 null=False, blank=False)
    assessed = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="assessments_as_assessed",
                                 related_query_name="assessments_as_assessed",
                                 null=False, blank=False)
    scales = models.ManyToManyField(Scale, verbose_name='معیارها')  # TODO delete, create every ScaleAnswer object when assessment is created
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name="assessments",
                               related_query_name="assessments", null=False, blank=False)

    unique_together = ("assessor", "assessed", "season")


class ScaleAnswer(models.Model):
    carried_on = models.BooleanField(default=False)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name="scale_answers",
                                   related_query_name="scale_answers")
    scale = models.ForeignKey(Scale, on_delete=models.CASCADE, null=False)
    qualitativeAnswer = models.CharField(max_length=100, null=True, blank=True)
    quantitativeAnswer = models.CharField(max_length=100, null=True, blank=True)


class PunishmentReward(models.Model):
    method = models.TextField(null=False, blank=False)
    type = models.NullBooleanField(null=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name="punishment_rewards",
                               related_query_name="punishment_rewards", null=False,
                               blank=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
