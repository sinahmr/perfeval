from django.contrib import admin


from . import models

admin.site.register(models.Unit)
# admin.site.register(models.UserManager)
admin.site.register(models.User)
admin.site.register(models.GeneralAdmin)
admin.site.register(models.Employee)
admin.site.register(models.UnitAdmin)

