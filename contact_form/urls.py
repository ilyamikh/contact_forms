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

    # Page for editing all student into
    path('edit_student/<int:student_id>/', views.edit_student, name='edit_student'),

    # Page for adding a new Guardian
    path('new_guardian/<int:student_id>/', views.new_guardian, name='new_guardian'),

    # Page for adding an Emergency Contact
    path('new_contact/<int:student_id>/', views.new_contact, name='new_contact'),

    # Page for adding a Person to Whom the Child may be Released
    path('new_pickup_contact/<int:student_id>/', views.new_pickup_contact, name='new_pickup_contact'),

    # Page for adding a Physician
    path('new_physician/<int:student_id>/', views.new_physician, name='new_physician'),

    # Page for editing an adult
    path('edit_adult/<int:adult_id>/', views.edit_adult, name='edit_adult'),

    # Limk for removing an adult
    path('remove_adult/<int:adult_id>/', views.remove_adult, name='remove_adult'),

    # Link for removing a student
    path('remove_student/<int:student_id>/', views.remove_student, name='remove_student'),

    # Page for viewing the Emergency Contacts form
    path('view_form/<int:student_id>/', views.view_form, name='view_form'),

    # Basic Child info page
    path('/user_initial/user_new_student_initial/', views.user_new_student_initial, name='user_new_student_initial'),

    # Child medical info page
    path(
        '/user_initial/user_student_medical_initial/<int:student_id>/',
        views.user_student_medical_initial,
        name='user_student_medical_initial'
    ),

    # New Guardian Page
    path(
        'user_initial/user_new_guardian_initial/<int:student_id>/',
        views.user_new_guardian_initial,
        name='user_new_guardian_initial'
    ),

    # New Pickup Person Page
    path(
        'user_initial/user_new_pickup_person_initial/<int:student_id>/',
        views.user_new_pickup_person_initial,
        name='user_new_pickup_person_initial'
    ),

    # New Contact Page
    path(
        'user_initial/user_new_contact_initial/<int:student_id>/',
        views.user_new_contact_initial,
        name='user_new_contact_initial'
    ),

    # New Physician Page
    path(
        'user_initial/user_new_doctor_initial/<int:student_id>/',
        views.user_new_doctor_initial,
        name='user_new_doctor_initial'
    ),
]
