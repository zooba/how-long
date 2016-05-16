"""
Definition of models.
"""

from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=512)

    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=512)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True)

    def __str__(self):
        return '{} ({})'.format(self.name, self.department)
