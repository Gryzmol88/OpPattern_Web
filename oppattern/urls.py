from django.urls import path
from . import views


app_name = 'oppattern'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('check_excel/', views.check_excel, name='check_excel'),
    path('daily_plan/', views.daily_plan, name='daily_plan'),
    path('daily_plan/show/<int:excel_id>/<date_choice>/', views.show_daily_plan, name='show_daily_plan'),
]
