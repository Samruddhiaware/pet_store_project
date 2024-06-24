from django.contrib import admin
from .models import pet

# Register your models here.
class Petadmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name', 'species')}

admin.site.register(pet, Petadmin)
# admin.site.register(Customer1)