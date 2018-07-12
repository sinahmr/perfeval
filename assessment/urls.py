from django.urls import path
from . import views

urlpatterns = [
    path('season/add/', views.AddSeasonView.as_view(), name='add_season'),
    path('scale/add/', views.AddScaleView.as_view(), name='add_scale'),
    path('employee/list/', views.EmployeesListView.as_view(), name='employee_list'),
    path('employee/show/<int:pk>/', views.ShowEmployeeView.as_view(), name='show_employee'),
    path('employee/home/', views.ShowMyDetailsView.as_view(), name='show_my_details'),
    path('eval/list/', views.AssessedsListView.as_view(), name='assessment_list'),
    path('create/<int:pk>/', views.CreateAssesment.as_view(), name='create_assessment'),
    # path('eval/<int:pk>', views.AssessorsListView.as_view(), name='assessors'),
    path('eval/<int:pk>/', views.DoAssessmentView.as_view(), name='assess'),
]
