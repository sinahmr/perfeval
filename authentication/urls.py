from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('unit/add/', views.AddUnitView.as_view(), name='add_unit'),
    path('employee/add/', views.AddEmployeeView.as_view(), name='add_employee'),
    path('user/update/', views.UpdateUsernameOrPasswordView.as_view(), name='user_update'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
