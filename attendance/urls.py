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
]
