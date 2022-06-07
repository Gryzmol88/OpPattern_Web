from django.contrib import admin
from .models import ExcelFile, Subject, ClassroomExcel

# Register your models here.


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('date', 'classroom', 'name', 'start_time', 'end_time')
    list_filter = ('excel_file', 'date', 'classroom', 'name')
    search_fields = ('date', 'classroom', 'name')
    date_hierarchy = 'date'

@admin.register(ExcelFile)
class ExcelFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')

@admin.register(ClassroomExcel)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('name',)
