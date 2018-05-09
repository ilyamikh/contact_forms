from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from contact_form.models import Group, Day, Student
from .forms import GroupForm, GroupDayForm

from datetime import date


@login_required
def attendance_view(request, student_id):
    """Displays a group of students with checkboxes for attendance (hopefully)"""
    student = Student.objects.get(id=student_id)
    days = student.day_set.order_by('-date')
    context = {'student': student, 'days': days}
    return render(request, 'attendance/attendance_view.html', context)


@login_required
def mark_student(request, student_id):
    """Display a student with corresponding checkboxes for attendance."""
    student = Student.objects.get(id=student_id)
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = GroupDayForm(initial={'date': date.today()})
    else:
        # POST data submitted; process data.
        form = GroupForm(data=request.POST)
        if form.is_valid():
            day = form.save(commit=False)
            day.student = student
            day.save()
        return HttpResponseRedirect(reverse('attendance:groups'))  # not sure about this

    context = {'student': student, 'form': form}  # or this
    return render(request, 'attendance/mark_student.html', context)


@login_required
def group(request, group_id):
    """Show all students in a group."""
    group = Group.objects.get(id=group_id)
    students = group.student_set.order_by('-last_name')
    context = {'group': group, 'students': students, }
    return render(request, 'attendance/group.html', context)


@login_required
def groups(request):
    """Show all groups."""
    groups = Group.objects.filter(owner=request.user).order_by('name')
    context = {'groups': groups}
    return render(request, 'attendance/groups.html', context)


@login_required
def new_group(request):
    """Add a new classroom."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = GroupForm()
    else:
        # POST data submitted; process data.
        form = GroupForm(data=request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.owner = request.user
            group.save()
            return HttpResponseRedirect(reverse('attendance:groups'))

    context = {'form': form}
    return render(request, 'attendance/new_group.html', context)

