import django_tables2
from django.utils.html import format_html

from app.models import Employee

class EmployeeNameColumn(django_tables2.Column):
    def render(self, value):
        return format_html('<a href="/employee/{0}/">{0}</a>', value)

class EmployeeTable(django_tables2.Table):
    class Meta:
        model = Employee
        attrs = {'class': 'paleblue'}

    name = EmployeeNameColumn()

