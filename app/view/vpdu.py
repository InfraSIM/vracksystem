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

from AutoDeployUI.models import ESXi

import sys
sys.path.append("../../")

title = "vRackSystem"

def getbasic(request):
    c = {}
    c.update(csrf(request))
    esxihosts = ESXi.objects.all()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'vpdu/vpdubasic.html',
        context_instance = RequestContext(request,
        {
            'esxihosts': esxihosts,
        })
    )

def getesxihost(request):
    c = {}
    c.update(csrf(request))
    esxihosts = ESXi.objects.all()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'vpdu/vpduesxi.html',
        context_instance = RequestContext(request,
        {
            'esxihosts': esxihosts,
        })
    )

def getpassword(request):
    c = {}
    c.update(csrf(request))
    esxihosts = ESXi.objects.all()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'vpdu/vpdupassword.html',
        context_instance = RequestContext(request,
        {
            'esxihosts': esxihosts,
        })
    )

def getmapping(request):
    c = {}
    c.update(csrf(request))
    esxihosts = ESXi.objects.all()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'vpdu/vpdumapping.html',
        context_instance = RequestContext(request,
        {
            'esxihosts': esxihosts,
        })
    )
