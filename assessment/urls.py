from django.urls import path
from . import views

urlpatterns = [
    path('season/add/', views.AddSeasonView.as_view(), name='add_season'),
    path('season/list/', views.SeasonListView.as_view(), name='list_season'),
    path('season/change/<int:pk>/', views.ChangeSeasonView.as_view(), name='change_season'),
    path('scale/add/', views.AddScaleView.as_view(), name='add_scale'),

    path('employee/list/', views.EmployeesListView.as_view(), name='employee_list'),
    path('employee/show/<int:pk>/', views.ShowEmployeeView.as_view(), name='show_employee'),

    path('create/<int:pk>/', views.CreateAssessment.as_view(), name='create_assessment'),

    path('eval/list/', views.AssessedsListView.as_view(), name='assessment_list'),
    path('eval/<int:pk>/', views.DoAssessmentView.as_view(), name='assess'),
    path('eval/judge/<int:pk>/', views.SetPunishmentRewardView.as_view(), name='punishment_reward'),
]
