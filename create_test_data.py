import os
import sys

CSV = '--csv' in sys.argv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HowLong.settings")

import django
django.setup()

import csv
from datetime import timedelta, datetime
from django.utils.timezone import now
from app.models import *
from random import randrange, choice

DEPARTMENTS = ['Sales', 'Marketing', 'Engineering']
NAME_FIRST_PART = ['St', 'J', 'K', 'P', 'S', 'M', 'Th', 'T', 'Ph', 'Cl', 'N', 'R', 'G']
NAME_MIDDLE_PART = ['ev', 'a', 'o', 'oa', 'ia', 'ick', 'eph', 'eo', 'ord', 'enn']
NAME_END_PART = ['e', 'o', 'an', 'en', 'al', 'eal', 'i', 'on', 'in', 'un', 'lund', 'ephus', 'ifer']

def generate_name():
    return choice(NAME_FIRST_PART) + choice(NAME_MIDDLE_PART) + choice(NAME_END_PART)

DEPARTMENT_AGE_RANGE = {
    'Sales': (10, 1000),
    'Marketing': (30, 2000),
    'Engineering': (100, 5000),
}



names = set()
def get_person():
    name = generate_name()
    while name in names:
        name = generate_name()
    names.add(name)

    dept = choice(DEPARTMENTS)

    ar = DEPARTMENT_AGE_RANGE[dept]
    d1, d2 = randrange(*ar), randrange(*ar)
    start, end = (d1, d2 - 100) if d1 > d2 else (d2, d1 - 100)
    start_date = now() - timedelta(days=start)
    if end > 0:
        end_date = now() - timedelta(days=end)
    else:
        end_date = None

    return name, dept, start_date, end_date

if CSV:
    filename = sys.argv[sys.argv.index('--csv') + 1]
    epoch = datetime(2001, 1, 1, tzinfo=now().tzinfo)
    with open(filename, 'w') as f:
        print('Name', 'Department', 'Start Date', 'End Date', sep=',', file=f)
        for _ in range(1000):
            name, dept, start_date, end_date = get_person()
            print(
                name,
                dept,
                (now() - start_date).days,
                (now() - end_date).days if end_date else '',
                sep=',',
                file=f
            )
else:
    departments = {}
    for dept in DEPARTMENTS:
        d = Department(name=dept)
        d.save()
        departments[dept] = d

    for _ in range(100):
        e = Employee()
        e.name, dept, e.start_date, e.end_date = get_person()

        e.department = departments[dept]

        e.save()

pass
