from django.db import models


class Student(models.Model):
    """The class represents the a chid's info, pointing to his application data"""
    internal_id = models.IntegerField(unique=True)  # Need to take care of this somehow
    is_active = models.BooleanField(default=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=300)  # don't want to make a separate model just for child address

    disabilities = models.CharField(max_length=600, blank=True)
    allergies = models.CharField(max_length=600, blank=True)
    emergency_medical_info = models.CharField(max_length=600, blank=True)
    medications = models.CharField(max_length=600, blank=True)
    additional_info = models.CharField(max_length=600, blank=True)

    health_insurance = models.CharField(max_length=300, blank=True)
    policy_number = models.CharField(max_length=300, blank=True)

    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the model."""
        return self.first_name + ' ' + self.last_name


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
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=300, blank=True)  # this should be autofilled on the page with child's address
    primary_number = models.CharField(max_length=20)  # is storing phone numbers as text ok?
    secondary_number = models.CharField(max_length=20, blank=True)
    email_address = models.EmailField(blank=True)  # why reinvent the wheel, right
    business_name = models.CharField(max_length=200, blank=True)
    work_number = models.CharField(max_length=20, blank=True)  # consider removing these defaults

    def __str__(self):
        """Return the string representation of the model."""
        return self.first_name + ' ' + self.last_name + ', ' + self.get_relationship_display()

