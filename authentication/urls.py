from django.urls import path

from . import views

urlpatterns = [
    path('employee/add/', views.AddEmployeeView.as_view(), name='employee_add'),
    path('user/update/', views.UpdateUsernameOrPasswordView.as_view(), name='user_update'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
