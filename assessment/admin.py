from django.contrib import admin
from . import models

admin.site.register(models.Assessment)
admin.site.register(models.ScaleAnswer)
admin.site.register(models.Scale)
admin.site.register(models.PunnishmentReward)
admin.site.register(models.QuantitativeCriterion)
admin.site.register(models.QualitativeCriterion)
admin.site.register(models.Season)