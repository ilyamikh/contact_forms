from django import forms

from .models import Student, Adult


class BasicChildInfoForm(forms.ModelForm):
    """Non-optional fields to create a Student"""
    class Meta:
        model = Student
        fields = [
            'first_name', 'last_name', 'date_of_birth',
            'street', 'city', 'state', 'zip',
            'internal_id',
        ]
        labels = {'first_name': 'First Name',
                  'last_name': 'Last Name',
                  'date_of_birth': 'Date of Birth MM/DD/YYYY',
                  'street': 'Street Address',
                  'city': 'City',
                  'state': 'State',
                  'zip': 'Zip Code',
                  'internal_id': 'Student ID',
                  }
        widgets = {
                'first_name': forms.TextInput(attrs={'required': True}),
                'last_name': forms.TextInput(attrs={'required': True}),
                'date_of_birth': forms.DateInput(attrs={'required': True}),
                   }


class UserBasicChildInfo(forms.ModelForm):
    """Non-optional fields for the User to complete."""
    class Meta:
        model = Student
        fields = [
            'first_name', 'last_name', 'date_of_birth',
            'street', 'city', 'state', 'zip',
            'internal_id',
        ]
        labels = {'first_name': 'First Name',
                  'last_name': 'Last Name',
                  'date_of_birth': 'Date of Birth MM/DD/YYYY',
                  'street': 'Street Address',
                  'city': 'City',
                  'state': 'State',
                  'zip': 'Zip Code',
                  'internal_id': 'Student ID',
                  }
        widgets = {
                'first_name': forms.TextInput(attrs={'required': True}),
                'last_name': forms.TextInput(attrs={'required': True}),
                'date_of_birth': forms.DateInput(attrs={'required': True}),
                'internal_id': forms.HiddenInput()
                   }


class ChildMedicalInfoForm(forms.ModelForm):
    """Child medical info, special conditions, and insurance."""
    class Meta:
        model = Student
        fields = ['disabilities', 'allergies', 'emergency_medical_info', 'medications', 'additional_info',
                  'health_insurance', 'policy_number', ]
        labels = {
            'disabilities': 'Special Disabilities (if any)',
            'allergies': 'Allergies (Including Medication Reaction)',
            'emergency_medical_info': 'Medical or Dietary Information Necessary in an Emergency Situation',
            'medications': 'Medication, Special Conditions',
            'additional_info': 'Additional Information on Special Needs of Child',
            'health_insurance': 'Health Insurance Coverage for Child or Medical Assistance Benefits',
            'policy_number': 'Policy Number (Required)',
        }
        widgets = {
            'health_insurance': forms.TextInput(attrs={'required': True}),
            'policy_number': forms.TextInput(attrs={'required': True}),
        }


class EditChildForm(forms.ModelForm):
    """Form to edit a Child, all fields, including status and ID."""
    class Meta:
        model = Student
        fields = [
            'internal_id', 'is_active',
            'first_name', 'last_name', 'date_of_birth',
            'street', 'city', 'state', 'zip',
            'disabilities', 'allergies', 'emergency_medical_info', 'medications', 'additional_info',
            'health_insurance', 'policy_number',
        ]
        labels = {
            'internal_id': 'Student ID',
            'is_active': 'Active',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'date_of_birth': 'Date of Birth',
            'street': 'Street Address',
            'city': 'City',
            'state': 'State',
            'zip': 'Zip Code',
            'disabilities': 'Special Disabilities (if any)',
            'allergies': 'Allergies (Including Medication Reaction)',
            'emergency_medical_info': 'Medical or Dietary Information Necessary in an Emergency Situation',
            'medications': 'Medication, Special Conditions',
            'additional_info': 'Additional Information on Special Needs of Child',
            'health_insurance': 'Health Insurance Coverage for Child or Medical Assistance Benefits',
            'policy_number': 'Policy Number (Required)',
        }
        widgets = {
                'first_name': forms.TextInput(attrs={'required': True}),
                'last_name': forms.TextInput(attrs={'required': True}),
                'date_of_birth': forms.DateInput(attrs={'required': True}),
                   }


class GuardianEntryForm(forms.ModelForm):
    """Form to add a parent/legal guardian."""
    class Meta:
        model = Adult
        fields = ['relationship', 'first_name', 'last_name',
                  'street', 'city', 'state', 'zip',
                  'primary_number', 'secondary_number', 'email_address',
                  'business_name', 'work_number',
                  'bus_street', 'bus_city', 'bus_state', 'bus_zip',
                  ]
        labels = {'relationship': 'Relationship to Child',
                  'first_name': 'First Name',
                  'last_name': 'Last Name',
                  'street': 'Street Address',
                  'city': 'City',
                  'state': 'State',
                  'zip': 'Zip Code',
                  'primary_number': 'Primary Phone Number',
                  'secondary_number': 'Secondary Phone Number',
                  'email_address': 'Email Address',
                  'business_name': 'Business Name',
                  'work_number': 'Work Number',
                  'bus_street': 'Street Address',
                  'bus_city': 'City',
                  'bus_state': 'State',
                  'bus_zip': 'Zip Code',
                  }
        widgets = {'relationship': forms.Select(),
                   }


class EditAdultForm(GuardianEntryForm):
    """Form to edit all adult fields."""
    GuardianEntryForm.Meta.fields.append('is_contact')
    GuardianEntryForm.Meta.labels['is_contact'] = 'Add this Person as Emergency Contact'


class ContactEntryForm(forms.ModelForm):
    """Form to add an emergency contact."""
    class Meta:
        model = Adult
        fields = [
            'relationship', 'first_name', 'last_name', 'primary_number',
        ]
        labels = {
            'relationship': 'Relationship to Child',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'primary_number': 'Primary Phone Number',
        }
        widgets = {
            'relationship': forms.Select(),
        }


class PickupPersonEntryForm(forms.ModelForm):
    """Form to add a pickup person."""
    class Meta:
        model = Adult
        fields = [
            'relationship', 'first_name', 'last_name', 'primary_number',
            'street', 'city', 'state', 'zip', 'is_contact'
        ]
        labels = {
            'relationship': 'Relationship to Child',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'street': 'Street Address',
            'city': 'City',
            'state': 'State',
            'zip': 'Zip Code',
            'primary_number': 'Primary Phone Number',
            'is_contact': 'Add this Person as Emergency Contact',
        }
        widgets = {
            'relationship': forms.Select(),
        }


class PhysicianEntryForm(forms.ModelForm):
    """Form to add Physician/Medical Care Provider."""
    class Meta:
        model = Adult
        fields = [
            'relationship', 'first_name', 'last_name', 'business_name',
            'bus_street', 'bus_city', 'bus_state', 'bus_zip',
            'primary_number',
        ]
        labels = {
            'relationship': 'Relationship to Child',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'business_name': 'Medical Care Provider Business Name',
            'bus_street': 'Street Address',
            'bus_city': 'City',
            'bus_state': 'State',
            'bus_zip': 'Zip Code',
            'primary_number': 'Primary Phone Number',
        }
        widgets = {
            'relationship': forms.Select(),
        }