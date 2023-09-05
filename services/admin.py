from django.contrib import admin
from .models import Services
from import_export.admin import ImportExportModelAdmin

@admin.register(Services)
class ViewAdmin(ImportExportModelAdmin):
    search_fields = ['serviceid', 'servicename', 'teamname', 'sre']