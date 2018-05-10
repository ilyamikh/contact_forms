from django import forms
from django.forms import formset_factory

from contact_form.models import Student, Group, Day


class GroupForm(forms.ModelForm):
    """Create/Edit classroom"""
    class Meta:
        model = Group
        fields = [
            'name',
        ]
        labels = {
            'name': 'Classroom Name',
        }


class StudentDayForm(forms.ModelForm):
    """Mark attendance and meals for the day on a group view"""
    class Meta:
        model = Day
        fields = [
             'date', 'attended', 'breakfast', 'lunch', 'pm_snack', 'supper', 'evening_snack',
        ]
        labels = {
            'date': 'Date',
            'attended': 'ATT',
            'breakfast': 'BR',
            'lunch': 'LU',
            'pm_snack': 'PM',
            'supper': 'SU',
            'evening_snack': 'EV',
        }


DayFormset = formset_factory(StudentDayForm)
