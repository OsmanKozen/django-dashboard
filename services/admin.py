from django.contrib import admin
from .models import Services
from import_export.admin import ImportExportModelAdmin

# Register your models here.
@admin.register(Services)
class ViewAdmin(ImportExportModelAdmin):
    pass