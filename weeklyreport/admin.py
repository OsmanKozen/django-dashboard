from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

@admin.register(Reports)
class ViewAdmin(ImportExportModelAdmin):
    search_fields = ['service', 'entry_owner', 'entry', 'team', 'manager']

@admin.register(Services)
class ViewAdmin(ImportExportModelAdmin):
    search_fields = ['servicename', 'username', 'teamname']

@admin.register(Users)
class ViewAdmin(ImportExportModelAdmin):
    search_fields = ['mail', 'username', 'teamname']

@admin.register(Teams)
class ViewAdmin(ImportExportModelAdmin):
    search_fields = ['teamname', 'unitname']

@admin.register(Units)
class ViewAdmin(ImportExportModelAdmin):
    search_fields = ['unitname']
    
@admin.register(Managers)
class ViewAdmin(ImportExportModelAdmin):
    search_fields = ['managername', 'teamname']