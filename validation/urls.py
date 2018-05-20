from django.urls import path
from . import views

urlpatterns = [
    path('objection/', views.request_new_assessment, name='request_new_assessment'),
    path('objection/list', views.objections_list, name='objections_list'),
    path('objection/<int:objection_id>', views.show_assessment_and_objection, name='show_assessment_and_objection'),
    path('inconsistency/list', views.inconsistency_list, name='inconsistency_list'),
    path('inconsistency/resolve/<int:inconsistency_id>', views.resolve_inconsistency, name='resolve_inconsistency'),
    path('criterion/list/<int:inconsistency_id>', views.resolve_inconsistency, name='resolve_inconsistency'),
]
