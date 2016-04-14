'''
*********************************************************
Copyright @ 2015 EMC Corporation All Rights Reserved
*********************************************************
'''

"""
Definition of views.
"""

from django.shortcuts import render
from django.template.context_processors import csrf
from django.http import HttpRequest
from django.template import RequestContext

from app.form.forms import NodeDeployForm

from AutoDeployUI.models import ESXi

title = "vRackSystem"


def uploadova(request):
    c = {}
    c.update(csrf(request))

    return render(
        request,
        '../templates/vnode/uploadova.html',
        {
            'title':title,
        }
    )

def vnodedeploy(request):
    c = {}
    c.update(csrf(request))
    esxihosts = ESXi.objects.all()
    deployForm = NodeDeployForm()

    return render(
        request,
        '../templates/vnode/vnodedeploy.html',
        {
            'title':title,
            'form':deployForm,
            'esxihosts': esxihosts,
            'message': "",
        }
    )

def vnodecontrol(request):
    c = {}
    c.update(csrf(request))
    esxihosts = ESXi.objects.all()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'vnode/vnodecontrol.html',
        context_instance = RequestContext(request,
        {
            'esxihosts': esxihosts,
        })
    )
