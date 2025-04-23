from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Prestadora)
admin.site.register(models.Telefono)
admin.site.register(models.Cliente)
admin.site.register(models.Tipo_equipo)
admin.site.register(models.Equipo)
admin.site.register(models.Tipo_respuesto_acc)