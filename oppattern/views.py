from datetime import datetime

import openpyxl
from django.shortcuts import render
from django.utils import timezone
from .models import ExcelFile, Subject


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


        #Create Subjects object from xlsx file.

        #Create Clasroom name.
        wb = openpyxl.load_workbook(excel_file, data_only=True)
        for active_sheet in wb.sheetnames:

            # activated sheet.
            sheet = wb[active_sheet]


            # add date to subject object

            for date_row in range(1, 300):
                temp_date = None
                temp_classroom = None
                temp_excel_file = None
                temp_name = None
                temp_start_time = None
                temp_start_endtime = None

                cell = sheet.cell(row=date_row, column=2)
                # Check is cell.value is datetieme. IF True. create objects.
                if isinstance(cell.value, datetime):
                    # Create subject date
                    temp_date = cell.value
                    # Create subject classroom
                    temp_classroom = active_sheet
                    # Create subject excel file
                    temp_excel_file = file




                    #Create subject name
                    for merged in sheet.merged_cells.ranges:
                        for column_number in range(3, 57):
                            cell = sheet.cell(row=date_row, column=column_number)
                            # Jeżeli koordynant komórki znajduje się w zakresie scalonych
                            # komórki zapisuje scalenie i przeskakuje do szukania dalszych scaleń.
                            if cell.coordinate in merged:
                                temp_name = merged.start_cell.value



                                sb = Subject()
                                sb.date = temp_date
                                sb.classroom = temp_classroom
                                sb.excel_file = temp_excel_file
                                sb.name = temp_name
                                #Create subject start_time.
                                sb.start_time = timezone.now().date()
                                #Create subject end_time.
                                sb.end_time = timezone.now().date()
                                sb.save()
                                break






        contetxt = {'title': title, 'date': date}

        return render(request, 'oppattern/upload.html', contetxt)


def read_excel(request):

    return render(request, 'oppattern/read_excel.html')
