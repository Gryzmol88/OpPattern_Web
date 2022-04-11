import openpyxl
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import SubjectForm
from .models import ExcelFile, Subject
from .operation import read_excel_file, check_date, check_mistake


# Create your views here.

def index(request):
    return render(request, 'oppattern/index.html')

def upload(request):
    if request.method != 'POST':

        return render(request, 'oppattern/upload.html')

    else:
        #Uploade xlsx file and save ExcelFile objects.
        excel_file = request.FILES['excel_file']
        title = excel_file.name
        file = ExcelFile()
        file.title = title
        file.date = timezone.now().date()
        file.save()
        date = file.date

        #Create object for db.
        for data in read_excel_file(excel_file):
            sb = Subject()
            sb.excel_file = file
            sb.classroom = data['classroom']
            sb.name = data['name']
            sb.date = data['date']
            sb.start_time = data['start_time']
            sb.end_time = data['end_time']
            sb.save()

        contetxt = {'title': title, 'date': date}

        return render(request, 'oppattern/upload.html', contetxt)

def check_excel(request):

    if request.method != 'POST':

        return render(request, 'oppattern/check_excel.html')

    else:
        #Uploade xlsx file.
        excel_file = request.FILES['excel_file']
        wb = openpyxl.load_workbook(filename=excel_file, data_only=True)
        wrong_subjects = check_mistake(wb)
        wrong_dates = check_date(wb)

        contetxt = {'wrong_dates': wrong_dates, 'wrong_subjects': wrong_subjects}
    return render(request, 'oppattern/check_excel.html', contetxt)

def daily_plan(request):
    daily_subjects = []
    if request.method != 'POST':
        form = SubjectForm()
    else:
        form = SubjectForm(request.POST)
        if form.is_valid():
            excel_file = form.cleaned_data['excel_file']
            date_choice = form.cleaned_data['date_choice']
            for object in Subject.objects.all():
                if object.excel_file == excel_file and object.date.date() == date_choice:
                    daily_subjects.append(object)

    context = {'form': form, 'daily_subjects': daily_subjects}

    return render(request, 'oppattern/daily_plan.html', context)

def show_daily_plan(request):
    # subject_file = Subject.objects.get(excel_file=excel_file_id)
    # #daily_subject = subject_file.objects.get(date=date)
    # context = {'subject_file': subject_file}
    return render(request, 'oppattern/show_daily_plan.html')
