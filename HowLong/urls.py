"""
Definition of urls for HowLong.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),

    url(r'^generate$', app.views.generate, name='generate'),
    url(r'^employees$', app.views.employees, name='employees'),
    url(r'^employee/(?P<employee_name>\w{0,100})/$', app.views.employee, name='employee'),

    url(r'^admin/', include(admin.site.urls)),
]

from django.conf import settings
from django.contrib.staticfiles import views

if settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', views.serve),
    ]
