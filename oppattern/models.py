from django.db import models
from django.utils import timezone
# Create your models here.

class ExcelFile(models.Model):
    title = models.CharField(max_length=250, default=None)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return self.title

class Subject(models.Model):
    excel_file = models.ForeignKey(ExcelFile, on_delete=models.CASCADE, default=None)
    classroom = models.CharField(max_length=100, default=None)
    date = models.DateTimeField(default=None)
    name = models.CharField(max_length=300, default=None)
    start_time = models.DateTimeField(default=None)
    end_time = models.DateTimeField(default=None)
    questionnaire = models.BooleanField(default=False)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return self.name
