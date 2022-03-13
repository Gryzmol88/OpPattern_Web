from django.shortcuts import render
from django.utils import timezone

from .models import ExcelFile
import openpyxl


# Create your views here.

def index(request):
    return render(request, 'oppattern/index.html')

def upload(request):
    if request.method != 'POST':

        return render(request, 'oppattern/upload.html')

    else:
        excel_file = request.FILES["excel_file"]

        title = excel_file.name
        file = ExcelFile()
        file.title = title
        file.date = timezone.now()
        file.save()
        date = file.date

        contetxt = {'title': title, 'date': date}

        return render(request, 'oppattern/upload.html', contetxt)

def read_excel(request, excel_file):
    wb = openpyxl.load_workbook(excel_file)
    active_sheet = wb.sheetnames[0]

    return render(request, 'oppattern/read_excel.html')
