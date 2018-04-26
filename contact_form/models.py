from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    """The class represents the a chid's info, pointing to his application data"""
    internal_id = models.IntegerField(unique=True)  # Need to take care of this somehow
    is_active = models.BooleanField(default=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()

    street = models.CharField(max_length=300)  # don't want to make a separate model just for child address
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=9)

    disabilities = models.CharField(max_length=600, blank=True)
    allergies = models.CharField(max_length=600, blank=True)
    emergency_medical_info = models.CharField(max_length=600, blank=True)
    medications = models.CharField(max_length=600, blank=True)
    additional_info = models.CharField(max_length=600, blank=True)

    health_insurance = models.CharField(max_length=300, blank=True)
    policy_number = models.CharField(max_length=300, blank=True)

    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return a string representation of the model."""
        return self.first_name + ' ' + self.last_name

    def get_mailing_address(self):
        """Returns a string of the complete mailing address."""
        return self.street + ', ' + self.city + ', ' + self.state + ' ' + self.zip


class Adult(models.Model):
    """The class holds the info for an adult somehow connected with the child"""
    child = models.ForeignKey(Student, on_delete=models.CASCADE)  # does it work simply like this, with internal key?
    is_active = models.BooleanField(default=True)  # do the adults need one too?

    RELATIONSHIP_CHOICES = (
        ('MO', 'Mother'),
        ('FA', 'Father'),
        ('LG', 'Legal Guardian'),
        ('EC', 'Emergency Contact'),
        ('PP', 'Person to whom the Child May be Released'),
        ('MP', 'Physician/Medical Care Provider'),
    )
    relationship = models.CharField(max_length=2, choices=RELATIONSHIP_CHOICES, default='MO')
    is_contact = models.BooleanField(default=True)  # switch mostly for pickup persons
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    street = models.CharField(max_length=300, blank=True)  # this should be autofilled on the page with child's address
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zip = models.CharField(max_length=9, blank=True)

    primary_number = models.CharField(max_length=20)  # is storing phone numbers as text ok?
    secondary_number = models.CharField(max_length=20, blank=True)
    email_address = models.EmailField(blank=True)  # why reinvent the wheel, right

    business_name = models.CharField(max_length=200, blank=True)
    work_number = models.CharField(max_length=20, blank=True)
    bus_street = models.CharField(max_length=300, blank=True)
    bus_city = models.CharField(max_length=100, blank=True)
    bus_state = models.CharField(max_length=2, blank=True)
    bus_zip = models.CharField(max_length=9, blank=True)

    def __str__(self):
        """Return the string representation of the model."""
        return self.first_name + ' ' + self.last_name + ', ' + self.get_relationship_display()

    def get_mailing_address(self):
        """Returns a string of the complete mailing address."""
        return self.street + ', ' + self.city + ', ' + self.state + ' ' + self.zip

    def get_business_address(self):
        """Returns a string of the complete business address."""
        return self.bus_street + ', ' + self.bus_city + ', ' + self.bus_state + ' ' + self.bus_zip
