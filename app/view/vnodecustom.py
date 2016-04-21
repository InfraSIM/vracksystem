'''
*********************************************************
Copyright @ 2015 EMC Corporation All Rights Reserved
*********************************************************
'''

"""
Definition of views.
"""

from datetime import datetime

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required

from AutoDeployUI.models import ESXi
esxihosts = ESXi.objects.all()

@login_required
def adddrive(request):
    c = {}
    c.update(csrf(request))
    assert isinstance(request, HttpRequest)
    return render(
        request,
        '../templates/vnodecustom/adddrive.html',
        context_instance = RequestContext(request,
        {
            'esxihosts': esxihosts,
        })
    )

@login_required
def addnic(request):
    c = {}
    c.update(csrf(request))
    assert isinstance(request, HttpRequest)
    return render(
        request,
        '../templates/vnodecustom/addnic.html',
        context_instance = RequestContext(request,
        {
            'esxihosts': esxihosts,
        })
    )

@login_required
def changemem(request):
    c = {}
    c.update(csrf(request))
    assert isinstance(request, HttpRequest)
    return render(
        request,
        '../templates/vnodecustom/changemem.html',
        context_instance = RequestContext(request,
        {
            'esxihosts': esxihosts,
        })
    )