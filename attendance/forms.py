from django import forms

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

