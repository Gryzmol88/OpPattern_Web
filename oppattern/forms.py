from django import forms
from django.forms import NumberInput

from .models import ExcelFile


class SubjectForm(forms.Form):
    excel_file = forms.ModelChoiceField(
        queryset=ExcelFile.objects.all(),
        initial=0,
    )
    date_choice = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
