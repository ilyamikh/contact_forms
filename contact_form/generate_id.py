from contact_form import models
import random
import datetime
import time


def generate_id():
    """Generates a 6-digit ID with the last 2 digits of the current year as the first 2 digits of ID"""
    year = get_year()
    lower = year * 10000
    upper = lower + 9999
    id = random.randint(lower, upper)

    while is_used(id):
        id = random.randint(lower, upper)

    return id


def is_used(id):
    """Checks if the ID has already been used"""
    id_list = []
    students = models.Student.objects.all()
    for student in students:
        id_list.append(student.student_id)

    if id in id_list:
        return True
    else:
        return False


def get_year():
    return int(datetime.datetime.fromtimestamp(time.time()).strftime('%Y')[2:])
