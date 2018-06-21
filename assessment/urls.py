from django.urls import path
from . import views

urlpatterns = [
     path('scale/add/', views.AddScaleView.as_view(), name='add_scale'),
     path('scale/list/', views.ScaleListView.as_view(), name='scale_list'),
     path('employee/list/', views.EmployeesListView.as_view(), name='employee_list'),
     path('employee/show/<int:pk>/', views.ShowEmployeeView.as_view(), name='show_employee'),
     path('employee/home/', views.ShowMyDetailsView.as_view(), name='show_my_details'),
     path('assessment/list/', views.AssessedsListView.as_view(), name='assessment_list'),
     path('assessment/<int:pk>', views.AssessorsListView.as_view(), name='assessors'),
]
