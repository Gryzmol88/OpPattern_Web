import datetime

import openpyxl
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import time

from .forms import SubjectForm
from .models import ExcelFile, Subject, ClassroomExcel
from .operation import read_excel_file, check_date, check_mistake


# Create your views here.

def index(request):
    return render(request, 'oppattern/index.html')

def upload(request):

    if request.method != 'POST':
        spinner_show = True
        context = {'spinner_show':spinner_show,}
        return render(request, 'oppattern/upload.html', context)

    else:

        #Uploade xlsx file and save ExcelFile objects.
        excel_file = request.FILES['excel_file']
        title = excel_file.name
        file = ExcelFile()
        file.title = title
        file.date = timezone.now()
        file.save()
        date = file.date

        #Get the list of class name from excel.
        classroom_list = []

        #Create object for db.
        for data in read_excel_file(excel_file):
            sb = Subject()
            sb.excel_file = file
            sb.classroom = data['classroom']
            #Create unique list with class name
            if data['classroom'] not in classroom_list:
                classroom_list.append(data['classroom'])
            sb.name = data['name']
            sb.date = data['date']
            sb.start_time = data['start_time']
            sb.end_time = data['end_time']
            sb.save()
        #Creat of list with existing object in model ClassroomExcel
        classroom_execel_list = []
        for object in ClassroomExcel.objects.all():
            classroom_execel_list.append(object.name)

        #Check if class name is in the object. If not create new object if yes, added file to existing object

        for class_name in classroom_list:
            if class_name in classroom_execel_list:
                classroom = ClassroomExcel.objects.get(name=class_name)
                file.classrooms.add(classroom)
                file.save()
            else:
                ce = ClassroomExcel(name=class_name)
                ce.save()
                classroom = ClassroomExcel.objects.get(name=class_name)
                file.classrooms.add(classroom)
                file.save()


        contetxt = {'title': title, 'date': date,}
        return render(request, 'oppattern/upload.html', contetxt)

def check_excel(request):

    if request.method != 'POST':

        return render(request, 'oppattern/check_excel.html')

    else:
        #Uploade xlsx file.
        excel_file_check = request.FILES['excel_file']
        wb = openpyxl.load_workbook(filename=excel_file_check, data_only=True)
        wrong_subjects = check_mistake(wb)
        wrong_dates = check_date(wb)

        contetxt = {'wrong_dates': wrong_dates, 'wrong_subjects': wrong_subjects}
    return render(request, 'oppattern/check_excel.html', contetxt)

def daily_plan(request):

    if request.method != 'POST':
        form = SubjectForm()
    else:
        form = SubjectForm(request.POST)
        if form.is_valid():
            excel_file = form.cleaned_data['excel_file']
            date_choice = form.cleaned_data['date_choice']
            excel_id = excel_file.id
            return redirect('oppattern:show_daily_plan',  excel_id=excel_id, date_choice=date_choice)

    context = {'form': form}

    return render(request, 'oppattern/daily_plan.html', context)

def show_daily_plan(request, excel_id, date_choice):

    date = datetime.datetime.strptime(date_choice, '%Y-%m-%d')
    excel_file = ExcelFile.objects.get(id=excel_id)
    plans = Subject.objects.filter(excel_file=excel_file).filter(date=date)
    #Create day of week
    days = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota', 'Niedziela']
    week_day = datetime.datetime.weekday(date)
    days[week_day]

    # Creat list of class for html pattern
    classroom_all = []
    for class_room in excel_file.classrooms.all():
        classroom_all.append(class_room.name)
    subjects = {}
    for class_name in classroom_all:
        subjects[class_name] = to_html_pattern(plans, class_name)



    context = {'time_list': make_time_description().keys(), 'subjects': subjects, 'date': date, 'week_day': days[week_day]}
    return render(request, 'oppattern/show_daily_plan.html', context)



def make_time_description():
    """Making time dict where key is time  and valueis column number."""
    time_list = []
    time_dict = {}
    skip = 15
    minute = -15
    hour = 7
    for x in range(0, 57):
        minute += skip
        if minute == 60:
            minute = 0
            hour += 1
        time_list.append(time(hour, minute))
    for column_number, sub_time in enumerate(time_list):
        time_dict[sub_time] = column_number

    return time_dict

def select_classroom(plan_list, classroom_name):
    """ Take Subject list and str wit classroom name. Return list with  dictionary"""
    subject_list = []
    #Transcrypt the models object to dict.
    for subject in plan_list:
        if subject.classroom == classroom_name:
            subject_dict = {'start_column': make_time_description()[subject.start_time],
                           'merged_cell': make_time_description()[subject.end_time]
                                          - make_time_description()[subject.start_time],
                           'subject_name': subject.name}
            subject_list.append(subject_dict)
            #Sort for start time.
            subject_list = sorted(subject_list, key=lambda x: x['start_column'])
    return subject_list

def to_html_pattern(plan_list, classroom_name):
    """Create  list pattern for HTML template """
    merged_cell = []
    object_list = []
    #Create list with numbers that should be removed.
    for object in select_classroom(plan_list, classroom_name):
        object_list.append(object)
        for merged_out in range(object['start_column']+1, object['start_column']+object['merged_cell']):
            merged_cell.append(merged_out)
    #Create list with 55 numbers (time from 7:00 to 20:30)
    pattern_list = [x for x in range(57)]
    #Removed numbers that are merged cells
    for removed in merged_cell:
        pattern_list.remove(removed)
    #Put the object in to start cells
    for object in object_list:
        for index, number in enumerate(pattern_list):
            if object['start_column'] == number:
                pattern_list[index] = object
    #Removed the numbers and put empty list.
    for number, object in enumerate(pattern_list):
        if type(object) is int:
            pattern_list[number] = []

    return pattern_list
