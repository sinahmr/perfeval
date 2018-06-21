from django.urls import path
from . import views

urlpatterns = [
    # path('criterion/add/', views.add_criterion, name='add_criterion'),
    # path('criterion/list/', views.criterion_list, name='criterion_list'),
     #path('employee/list/', views.employee_list, name='employee_list'),
     path('employee/show/<int:pk>', views.ShowEmployeeView.as_view(), name='show_employee'),
     path('employee/show/', views.ShowMyDetailsView.as_view(), name='show_my_details'),
    path('eval/list/', views.EmployeesListView.as_view(), name='assessment_list'),
    # path('eval/<int:employee_id>', views.assess, name='assess'),
]
