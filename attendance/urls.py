"""Defines URL patterns for attendance"""


from django.urls import path
from . import views

app_name = 'attendance'
urlpatterns = [
    # New group
    path('new_group/', views.new_group, name='new_group'),
    # all classrooms
    path('groups/', views.groups, name='groups'),
    # classroom view
    path('group/<int:group_id>/', views.group, name='group'),
    # mark attendance view
    path('attendance_view/<int:group_id>/', views.attendance_view, name='attendance_view'),
    # mark student view
    path('mark_student/<int:student_id>/', views.mark_student, name='mark_student'),
]
