from django.urls import path
from . import views

urlpatterns = [
    path('user/add/', views.add_user, name='add_user'),
    path('user/change/', views.change_username_or_password, name='change_username_or_password'),
    path('login/', views.login, name='login'),
    path('user/delete/<int:user_id>', views.delete_user),  # TODO delete this API
]
