import os
import sys

raise ValueError()

if sys.platform == 'win32':
    import ctypes
    ctypes.WinDLL('kernel32').AddDllDirectory(os.path.join(os.path.abspath(__file__), '..', 'FreeTDS'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HowLong.settings")

import django
django.setup()

from datetime import timedelta
from django.utils.timezone import now
from app.models import *
from random import randrange, choice

DEPARTMENTS = ['Sales', 'Marketing', 'Engineering']
NAME_FIRST_PART = ['St', 'J', 'K', 'P', 'S', 'M', 'Th', 'T']
NAME_MIDDLE_PART = ['ev', 'a', 'o', 'o', 'oa', 'ia', 'ick', 'eph']
NAME_END_PART = ['e', 'o', 'an', 'en', 'al', 'eal', 'i', '']

departments = []
for dept in DEPARTMENTS:
    d = Department(name=dept)
    departments.append(d)
    d.save()

def generate_name():
    return choice(NAME_FIRST_PART) + choice(NAME_MIDDLE_PART) + choice(NAME_END_PART)

DEPARTMENT_AGE_RANGE = {
    'Sales': (10, 1000),
    'Marketing': (30, 2000),
    'Engineering': (100, 5000),
}

names = set()
for _ in range(100):
    e = Employee()
    e.name = generate_name()
    while e.name in names:
        e.name = generate_name()
    names.add(e.name)
    
    dept = choice(departments)
    e.department = dept

    ar = DEPARTMENT_AGE_RANGE[dept.name]
    d1, d2 = randrange(*ar), randrange(*ar)
    start, end = (d1, d2 - 100) if d1 > d2 else (d2, d1 - 100)
    e.start_date = now() - timedelta(days=start)
    if end > 0:
        e.end_date = now() - timedelta(days=end)

    e.save()