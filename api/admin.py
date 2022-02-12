from django.contrib import admin
from . import models

admin.site.register(models.Pets)
admin.site.register(models.PetsPhoto)
