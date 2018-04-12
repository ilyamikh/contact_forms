from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse


from .models import Student
from .forms import BasicChildInfoForm, GuardianEntryForm, ContactEntryForm, PickupPersonEntryForm, PhysicianEntryForm, ChildMedicalInfoForm


def index(request):
    """The home page for all users"""
    return render(request, 'contact_form/index.html')


def students(request):
    """Show all students."""
    students = Student.objects.order_by('date_added')
    context = {'students': students}
    return render(request, 'contact_form/students.html', context)


def student(request, student_id):
    """Show a single student and his info."""
    student = Student.objects.get(id=student_id)
    adults = student.adult_set.order_by('-last_name')
    context = {'student': student, 'adults': adults}
    return render(request, 'contact_form/student.html', context)


def view_form(request, student_id):
    """Display the emergency contact form."""
    student = Student.objects.get(id=student_id)
    adults = student.adult_set.order_by('-last_name')
    context = {'student': student, 'adults': adults}
    return render(request, 'contact_form/view_form.html', context)


def new_student(request):
    """Add a new Student."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = BasicChildInfoForm()
    else:
        # POST data submited; process data.
        form = BasicChildInfoForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('contact_form:students'))

    context = {'form': form}
    return render(request, 'contact_form/new_student.html', context)


def student_medical(request, student_id):
    """Fill in Student medical info."""
    student = Student.objects.get(id=student_id)

    if request.method != 'POST':
        # Initial request; pre-fill form with the current student.
        form = ChildMedicalInfoForm(instance=student)
    else:
        # POST data submitted; process data.
        form = ChildMedicalInfoForm(instance=student, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('contact_form:student', args=[student_id]))

    context = {'student': student, 'form': form}
    return render(request, 'contact_form/student_medical.html', context)


def new_guardian(request, student_id):
    """Add a Student's Guardian"""
    student = Student.objects.get(id=student_id)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = GuardianEntryForm()
    else:
        # POST data submitted; process data.
        form = GuardianEntryForm(data=request.POST)
        if form.is_valid():
            new_guardian = form.save(commit=False)
            new_guardian.child = student
            new_guardian.save()
            return HttpResponseRedirect(reverse('contact_form:student', args=[student_id]))

    context = {'student': student, 'form': form}
    return render(request, 'contact_form/new_guardian.html', context)


def new_contact(request, student_id):
    """Add a Student's emergency contact"""
    student = Student.objects.get(id=student_id)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = ContactEntryForm()
    else:
        # POST data submitted; process data.
        form = ContactEntryForm(data=request.POST)
        if form.is_valid():
            new_contact = form.save(commit=False)
            new_contact.child = student
            new_contact.save()
            return HttpResponseRedirect(reverse('contact_form:student', args=[student_id]))

    context = {'student': student, 'form': form}
    return render(request, 'contact_form/new_contact.html', context)


def new_pickup_contact(request, student_id):
    """Add a person to whom the Child may be released."""
    student = Student.objects.get(id=student_id)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = PickupPersonEntryForm()
    else:
        # POST data submitted; process data.
        form = PickupPersonEntryForm(data=request.POST)
        if form.is_valid():
            new_pickup_contact = form.save(commit=False)
            new_pickup_contact.child = student
            new_pickup_contact.save()
            return HttpResponseRedirect(reverse('contact_form:student', args=[student_id]))

    context = {'student': student, 'form': form}
    return render(request, 'contact_form/new_pickup_contact.html', context)


def new_physician(request, student_id):
    """Add a physician/medical care provider."""
    student = Student.objects.get(id=student_id)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = PhysicianEntryForm()
    else:
        # POST data submitted; process data.
        form = PhysicianEntryForm(data=request.POST)
        if form.is_valid():
            new_physician = form.save(commit=False)
            new_physician.child = student
            new_physician.save()
            return HttpResponseRedirect(reverse('contact_form:student', args=[student_id]))

    context = {'student': student, 'form': form}
    return render(request, 'contact_form/new_physician.html', context)
