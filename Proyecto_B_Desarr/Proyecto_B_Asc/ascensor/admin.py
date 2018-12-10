from django.contrib import admin

from .models import Cliente, Orden, Tecnico

# Register your models here.
admin.site.register(Cliente)
admin.site.register(Orden)
admin.site.register(Tecnico)
