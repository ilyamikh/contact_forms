from django.db import models
from django.contrib.auth.models import User

from contact_form.models import Student


class Group(models.model):
    """Represents a classroom with a list of students."""
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)


class Day(models.model):
    """Represents a single day of operation."""
    date = models.DateField()  # is this an efficient way to keep track of the attendance?
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # not feeling good about this cascade
    # The default values will be set through views depending on child eligibility
    attended = models.BooleanField(blank=True)
    breakfast = models.BooleanField(blank=True)
    lunch = models.BooleanField(blank=True)
    pm_snack = models.BooleanField(blank=True)
    supper = models.BooleanField(blank=True)
    evening_snack = models.BooleanField(blank=True)
