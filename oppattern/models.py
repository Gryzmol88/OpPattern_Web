from django.db import models
from django.utils import timezone
# Create your models here.

class ClassroomExcel(models.Model):
    name = models.CharField(max_length=100, default=None)

    class Meta:
        ordering = ('-name',)

    def __str__(self):
        return self.name


class ExcelFile(models.Model):
    title = models.CharField(max_length=250, default=None)
    date = models.DateTimeField(default=timezone.now)
    classrooms = models.ManyToManyField(ClassroomExcel)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return f'{self.date.strftime("%Y-%m-%d %H:%M:%S")} : {self.title}'


class Subject(models.Model):
    excel_file = models.ForeignKey(ExcelFile, on_delete=models.CASCADE, default=None)
    classroom = models.CharField(max_length=100, default=None)
    date = models.DateTimeField(default=None)
    name = models.CharField(max_length=300, default=None)
    start_time = models.TimeField(default=None)
    end_time = models.TimeField(default=None)
    questionnaire = models.BooleanField(default=False)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return self.name
