from django.contrib import admin
from .models import ExcelFile, Subject

# Register your models here.


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('date', 'classroom', 'name')
    list_filter = ('excel_file', 'date', 'classroom', 'name')
    search_fields = ('date', 'classroom', 'name')

@admin.register(ExcelFile)
class ExcelFileAdmin(admin.ModelAdmin):
    list_display = ('date', 'title')