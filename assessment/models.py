from django.db import models

# Create your models here.
from authentication.models import Employee

class Season(models.Model):
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()

class QualitativeCriterion(models.Model):
    choices = models.CharField(verbose_name='انتخاب ها', max_length=20, null=False, blank=False)
    interpretation = models.TextField()

class QuantitativeCriterion(models.Model):
    formula = models.CharField(verbose_name='فرمول', max_length=20, null=False, blank=False)
    interpretation = models.TextField()

class Scale(models.Model):
    title = models.CharField(verbose_name='عنوان', max_length=20, null=False)
    description = models.TextField()
    qualitativeCriterion = models.ForeignKey(QualitativeCriterion)
    quantitativeCriterion = models.ForeignKey(QuantitativeCriterion)

class Assessment(models.Model):
    assessor = models.ForeignKey(Employee, related_name= "assessments_as_assessor" , related_query_name="assessments_as_assessor" ,
                                 null=False, blank= False)
    assessed = models.ForeignKey(Employee, related_name= "assessments_as_assessed" , related_query_name="assessments_as_assessed" ,
                                 null=False, blank= False)
    season = models.ForeignKey(Season, related_name="assessments", related_query_name="assessments" , null=False , blank= False)

    unique_together = ("assessor", "assessed", "season")


class ScaleAnswer(models.Model):
    assessment = models.ForeignKey(Assessment, related_name="scale_answers", related_query_name="scale_answers")
    scale = models.OneToOneField(Scale, null=False)
    qualitativeAnswer = models.CharField(max_length=100,null=False,blank=False)
    quantitativeAnswer = models.CharField(max_length=100,null=False,blank=False)

class PunnishmentReward(models.Model):
    method = models.TextField(null=False, blank=False)
    type = models.BooleanField(null=True)
    season = models.ForeignKey(Season, related_name="punishment_rewards", related_query_name="punishment_rewards", null=False,
                               blank=False)
    employee = models.ForeignKey(Employee)

