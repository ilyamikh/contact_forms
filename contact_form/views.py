import random, datetime, time

from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Student, Adult
from .forms import GuardianEntryForm, ContactEntryForm, PickupPersonEntryForm, PhysicianEntryForm
from .forms import BasicChildInfoForm, ChildMedicalInfoForm, EditChildForm, EditAdultForm
from .forms import UserBasicChildInfo


def index(request):
    """The home page for all users"""
    return render(request, 'contact_form/index.html')


@login_required
def students(request):
    """Show all students."""
    students = Student.objects.filter(owner=request.user).order_by('date_added')
    context = {'students': students}
    return render(request, 'contact_form/students.html', context)


def check_owner(student, request):
    if student.owner != request.user:
        raise Http404


@login_required
def student(request, student_id):
    """Show a single student and his info."""
    student = Student.objects.get(id=student_id)
    check_owner(student, request)
    adults = student.adult_set.order_by('-last_name')
    context = {'student': student, 'adults': adults}
    return render(request, 'contact_form/student.html', context)


@login_required
def view_form(request, student_id):
    """Display the emergency contact form."""
    student = Student.objects.get(id=student_id)
    check_owner(student, request)
    adults = student.adult_set.order_by('-last_name')

    contacts = []
    pickups = []
    parents = []
    for adult in adults:
        if adult.relationship == "EC" or (adult.relationship == "PP" and adult.is_contact):
            contacts.append(adult)
        elif adult.relationship in ["MO", "FA", "LG"]:
            parents.append(adult)

    # Redundant loop
    for adult in adults:
        if adult.relationship == "PP":
            pickups.append(adult)

    context = {
                'student': student,
                'adults': adults,
                'contacts': contacts,
                'pickups': pickups,
                'parents': parents,
               }
    return render(request, 'contact_form/view_form.html', context)


@login_required
def new_student(request):
    """Add a new Student."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = BasicChildInfoForm(initial={'internal_id': generate_id()})
    else:
        # POST data submitted; process data.
        form = BasicChildInfoForm(data=request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.owner = request.user
            student.save()
            return HttpResponseRedirect(reverse('contact_form:new_guardian', args=[student.id]))

    context = {'form': form}
    return render(request, 'contact_form/new_student.html', context)


@login_required
def user_new_student_initial(request):
    """User adds a new student for the first time."""
    if request.method != 'POST':
        # No data submitted, create a blank form
        form = UserBasicChildInfo(initial={'internal_id': generate_id()})
    else:
        # POST data submitted; process data.
        form = UserBasicChildInfo(data=request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.owner = request.user
            student.save()
            # Take the user to enter student medical info next
            return HttpResponseRedirect(reverse('contact_form:user_student_medical_initial', args=[student.id]))

    context = {'form': form}
    return render(request, 'contact_form/user_initial/user_new_student_initial.html', context)


@login_required
def user_student_medical_initial(request, student_id):
    """User enters student medical info for the first time."""
    student = Student.objects.get(id=student_id)
    check_owner(student, request)

    if request.method != 'POST':
        # Initial request; pre-fill form with the current student.
        form = ChildMedicalInfoForm(instance=student)
    else:
        # POST data submitted; process data.
        form = ChildMedicalInfoForm(instance=student, data=request.POST)
        if form.is_valid():
            form.save()
            # Take the user to enter the guardian info next
            return HttpResponseRedirect(reverse('contact_form:user_new_guardian_initial', args=[student_id]))

    context = {'student': student, 'form': form}
    return render(request, 'contact_form/user_initial/user_student_medical_initial.html', context)


@login_required
def user_new_guardian_initial(request, student_id):
    """User enters the initial first guardian."""
    student = Student.objects.get(id=student_id)
    check_owner(student, request)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = GuardianEntryForm(initial={
            'street': student.street, 'city': student.city, 'state': student.state, 'zip': student.zip,
        })
    else:
        # POST data submitted; process data.
        form = GuardianEntryForm(data=request.POST)
        if form.is_valid() and "submit" in request.POST:
            new_guardian = form.save(commit=False)
            new_guardian.child = student
            new_guardian.save()
            return HttpResponseRedirect(reverse('contact_form:user_new_pickup_person_initial', args=[student_id]))
        elif form.is_valid() and "add_another" in request.POST:
            new_guardian = form.save(commit=False)
            new_guardian.child = student
            new_guardian.save()
            return HttpResponseRedirect(reverse('contact_form:user_new_guardian_initial', args=[student_id]))

    context = {'student': student, 'form': form}
    return render(request, 'contact_form/user_initial/user_new_guardian_initial.html', context)


@login_required
def user_new_pickup_person_initial(request, student_id):
    """Users enters the initial pickup person."""
    student = Student.objects.get(id=student_id)
    check_owner(student, request)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = PickupPersonEntryForm(initial={'relationship': 'PP'})
    else:
        # POST data submitted; process data.
        form = PickupPersonEntryForm(data=request.POST)
        if form.is_valid() and "submit" in request.POST:
            new_pickup_contact = form.save(commit=False)
            new_pickup_contact.child = student
            new_pickup_contact.save()
            return HttpResponseRedirect(reverse('contact_form:user_new_contact_initial', args=[student_id]))
        elif form.is_valid() and "add_another" in request.POST:
            new_pickup_contact = form.save(commit=False)
            new_pickup_contact.child = student
            new_pickup_contact.save()
            return HttpResponseRedirect(reverse('contact_form:user_new_pickup_person_initial', args=[student_id]))

    context = {'student': student, 'form': form}
    return render(request, 'contact_form/user_initial/user_new_pickup_person_initial.html', context)


@login_required
def user_new_contact_initial(request, student_id):
    """User enters the initial emergency contact."""
    student = Student.objects.get(id=student_id)
    check_owner(student, request)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = ContactEntryForm(initial={'relationship': 'EC'})
    else:
        # POST data submitted; process data.
        form = ContactEntryForm(data=request.POST)
        if form.is_valid() and "submit" in request.POST:
            new_contact = form.save(commit=False)
            new_contact.child = student
            new_contact.save()
            return HttpResponseRedirect(reverse('contact_form:user_new_doctor_initial', args=[student_id]))
        elif form.is_valid() and "add_another" in request.POST:
            new_contact = form.save(commit=False)
            new_contact.child = student
            new_contact.save()
            return HttpResponseRedirect(reverse('contact_form:user_new_contact_initial', args=[student_id]))

    context = {'student': student, 'form': form}
    return render(request, 'contact_form/user_initial/user_new_contact_initial.html', context)


@login_required
def user_new_doctor_initial(request, student_id):
    """User enters doctor info for the first time."""
    student = Student.objects.get(id=student_id)
    check_owner(student, request)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = PhysicianEntryForm(initial={'relationship': 'MP'})
    else:
        # POST data submitted; process data.
        form = PhysicianEntryForm(data=request.POST)
        if form.is_valid():
            new_physician = form.save(commit=False)
            new_physician.child = student
            new_physician.is_contact = False
            new_physician.work_number = new_physician.primary_number  # To keep the form consistent
            new_physician.save()
            return HttpResponseRedirect(reverse('contact_form:view_form', args=[student_id]))

    context = {'student': student, 'form': form}
    return render(request, 'contact_form/user_initial/user_new_doctor_initial.html', context)


@login_required
def student_medical(request, student_id):
    """Fill in Student medical info."""
    student = Student.objects.get(id=student_id)
    check_owner(student, request)

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


@login_required
def edit_student(request, student_id):
    """Edit all student fields."""
    student = Student.objects.get(id=student_id)
    check_owner(student, request)

    if request.method != 'POST':
        # Initial request; pre-fill form with the current student.
        form = EditChildForm(instance=student)
    else:
        # POST data submitted, process data.
        form = EditChildForm(instance=student, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('contact_form:student', args=[student_id]))

    context = {'student': student, 'form': form}
    return render(request, 'contact_form/edit_student.html', context)


@login_required
def new_guardian(request, student_id):
    """Add a Student's Guardian"""
    student = Student.objects.get(id=student_id)
    check_owner(student, request)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = GuardianEntryForm(initial={
            'street': student.street, 'city': student.city, 'state': student.state, 'zip': student.zip,
        })
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


@login_required
def edit_adult(request, adult_id):
    """Edit all adult fields."""
    adult = Adult.objects.get(id=adult_id)
    student = adult.child
    check_owner(student, request)

    if request.method != 'POST':
        # Initial request; pre-fill form with the current student.
        form = EditAdultForm(instance=adult)
    else:
        # POST data submitted, process data.
        form = EditAdultForm(instance=adult, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('contact_form:student', args=[student.id]))

    context = {'adult': adult, 'student': student, 'form': form}
    return render(request, 'contact_form/edit_adult.html', context)


@login_required
def remove_adult(request, adult_id):
    adult = Adult.objects.get(id=adult_id)
    student = adult.child
    check_owner(student, request)
    adult.delete()

    return HttpResponseRedirect(reverse('contact_form:student', args=[student.id]))


@login_required
def remove_student(request, student_id):
    student = Student.objects.get(id=student_id)
    check_owner(student, request)
    student.delete()

    return HttpResponseRedirect(reverse('contact_form:students'))


@login_required
def new_contact(request, student_id):
    """Add a Student's emergency contact"""
    student = Student.objects.get(id=student_id)
    check_owner(student, request)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = ContactEntryForm(initial={'relationship': 'EC'})
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


@login_required
def new_pickup_contact(request, student_id):
    """Add a person to whom the Child may be released."""
    student = Student.objects.get(id=student_id)
    check_owner(student, request)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = PickupPersonEntryForm(initial={'relationship': 'PP'})
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


@login_required
def new_physician(request, student_id):
    """Add a physician/medical care provider."""
    student = Student.objects.get(id=student_id)
    check_owner(student, request)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = PhysicianEntryForm(initial={'relationship': 'MP'})
    else:
        # POST data submitted; process data.
        form = PhysicianEntryForm(data=request.POST)
        if form.is_valid():
            new_physician = form.save(commit=False)
            new_physician.child = student
            new_physician.is_contact = False
            new_physician.work_number = new_physician.primary_number  # To keep the form consistent
            new_physician.save()
            return HttpResponseRedirect(reverse('contact_form:student', args=[student_id]))

    context = {'student': student, 'form': form}
    return render(request, 'contact_form/new_physician.html', context)


def generate_id():
    """Generates a 6-digit ID with the last 2 digits of the current year as the first 2 digits of ID"""
    year = get_year()
    lower = year * 10000
    upper = lower + 9999
    id_num = random.randint(lower, upper)

    while is_used(id_num):
        id_num = random.randint(lower, upper)

    return id_num


def is_used(id_num):
    """Checks if the ID has already been used"""
    id_list = []
    students = Student.objects.all()
    for student in students:
        id_list.append(student.internal_id)

    if id_num in id_list:
        return True
    else:
        return False


def get_year():
    """Returns integer of last two digits of the current year"""
    return int(datetime.datetime.fromtimestamp(time.time()).strftime('%Y')[2:])
