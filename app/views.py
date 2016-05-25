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
from datetime import datetime

from app.models import Department, Employee

def home(request):
    """Renders the home page."""
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
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
            'year':datetime.now().year,
            'company': os.getenv('COMPANY_NAME', 'Our Company')
        }
    )

def employees(request):
    """Renders the contact page."""
    return render(
        request,
        'app/employees.html',
        {
            'title':'Employees',
            'message':'Your employee page.',
            'year':datetime.now().year,
            'company': os.getenv('COMPANY_NAME', 'Our Company'),
            'employees': Employee.objects.all(),
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
            'year':datetime.now().year,
            'company': os.getenv('COMPANY_NAME', 'Our Company'),
            'output': output,
        }
    )
