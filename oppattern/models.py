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
