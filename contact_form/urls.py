"""Defines url patterns for contact_form."""

from django.urls import path

from . import views

app_name = 'contact_form'
urlpatterns = [
    # Home page.
    path('', views.index, name='index'),

    # Show all students.
    path('students/', views.students, name='students'),

    # Detail page for a single student.
    path('students/<int:student_id>/', views.student, name='student'),

    # Page for adding a new Student
    path('new_student/', views.new_student, name='new_student'),

    # Page for adding student medical info
    path('student_medical/<int:student_id>/', views.student_medical, name='student_medical'),

    # Page for adding a new Guardian
    path('new_guardian/<int:student_id>/', views.new_guardian, name='new_guardian'),

    # Page for adding an Emergency Contact
    path('new_contact/<int:student_id>/', views.new_contact, name='new_contact'),

    # Page for adding a Person to Whom the Child may be Released
    path('new_pickup_contact/<int:student_id>/', views.new_pickup_contact, name='new_pickup_contact'),

    # Page for adding a Physician
    path('new_physician/<int:student_id>/', views.new_physician, name='new_physician'),

    # Page for viewing the Emergency Contacts form
    path('view_form/<int:student_id>/', views.view_form, name='view_form'),
]
