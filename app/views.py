"""
Definition of views.
"""

import os
import subprocess
import sys
import traceback

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.utils.timezone import now
from datetime import timedelta

from app.models import Department, Employee
from app.tables import EmployeeTable

from app.prediction import length_of_employment

def home(request):
    """Renders the home page."""
    return render(
        request,
        'app/index.html',
        {
            'title': 'Home Page',
            'year': now().year,
            'company': os.getenv('COMPANY_NAME', 'Our Company')
        }
    )

def contact(request):
    """Renders the contact page."""
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year': now().year,
            'company': os.getenv('COMPANY_NAME', 'Our Company')
        }
    )


def employees(request):
    """Renders the employee list."""
    return render(
        request,
        'app/employees.html',
        {
            'title':'Employees',
            'message':'Your employee page.',
            'year': now().year,
            'company': os.getenv('COMPANY_NAME', 'Our Company'),
            'employees': EmployeeTable(Employee.objects.all()),
        }
    )

def employee(request, employee_name):
    """Renders details about a single employee."""
    e = Employee.objects.get(name=employee_name)
    e.refresh_from_db()

    expected_days = timedelta(days=length_of_employment(e.department.name, e.start_date))

    return render(
        request,
        'app/employee.html',
        {
            'title': '{.name} Info'.format(e),
            'message': 'unexpected message',
            'year': now().year,
            'company': os.getenv('COMPANY_NAME', 'Our Company'),
            'name': e.name,
            'department': e.department.name,
            'start_date': e.start_date,
            'end_date': e.end_date,
            'expected_days': expected_days,
            'total_days': ((e.end_date or now().date()) - e.start_date).days,
            'expected_end_date': (e.start_date + expected_days)
        }
    )

def generate(request):
    script = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'create_test_data.py')
    try:
        subprocess.Popen([sys.executable, script])
    except Exception:
        output = traceback.format_exc()
    else:
        output = ""

    return render(
        request,
        'app/generating.html',
        {
            'title':'Generate Test Data',
            'year': now().year,
            'company': os.getenv('COMPANY_NAME', 'Our Company'),
            'output': output,
        }
    )
