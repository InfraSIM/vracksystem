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
from django.template.context_processors import csrf
from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from AutoDeployUI.models import ESXi

import sys
sys.path.append("../../")

title = "vRackSystem"

@login_required
def getbasic(request):
    c = {}
    c.update(csrf(request))
    esxihosts = ESXi.objects.all()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'vpdu/vpdubasic.html',
        {
            'esxihosts': esxihosts,
        }
    )

@login_required
def getesxihost(request):
    c = {}
    c.update(csrf(request))
    esxihosts = ESXi.objects.all()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'vpdu/vpduesxi.html',
        {
            'esxihosts': esxihosts,
        }
    )

@login_required
def getpassword(request):
    c = {}
    c.update(csrf(request))
    esxihosts = ESXi.objects.all()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'vpdu/vpdupassword.html',
        {
            'esxihosts': esxihosts,
        }
    )

@login_required
def getmapping(request):
    c = {}
    c.update(csrf(request))
    esxihosts = ESXi.objects.all()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'vpdu/vpdumapping.html',
        {
            'esxihosts': esxihosts,
        }
    )
