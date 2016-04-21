'''
*********************************************************
Copyright @ 2015 EMC Corporation All Rights Reserved
*********************************************************
'''

"""
Definition of views.
"""
import os
from datetime import datetime

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template.context_processors import csrf
from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.template import RequestContext

from AutoDeployUI.models import ESXi

from app.form.forms import ESXiAddForm
from app.form.forms import ESXiEditForm
from django.contrib.auth.decorators import login_required

title = "vRack System"

@login_required
def esxi(request):
    esxiHome = ESXi.objects.all()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        '../templates/esxi/esxiview.html',
        context_instance = RequestContext(request,
        {
            'title':title,
            'esxiHosts':esxiHome,
        })
    )

@login_required
def esxiadd(request):
    c = {}
    c.update(csrf(request))
    if request.method == "POST":
        esxiAddForm = ESXiAddForm(request.POST)
        if esxiAddForm.is_valid():
            esxihost = request.POST['esxihost']
            username = request.POST['username']
            password = request.POST['password']

            if str(esxihost)!="None" and str(username)!="None" and str(password)!="None":
                esxi = ESXi(esxiIP=str(esxihost),username=str(username),password=str(password))
                try:
                    esxi.save()
                    return HttpResponseRedirect('../esxi', c)
                except Exception, e:
                    error_message = "ESXi {} already exists.".format(esxihost)
                    return render(
                    request,
                        '../templates/esxi/esxiadd.html',
                        {
                            'title':title,
                            'form':esxiAddForm,
                            'error_message': error_message,
                        }
                    )

    else:
        esxiAddForm = ESXiAddForm()

    return render(
        request,
        '../templates/esxi/esxiadd.html',
        {
            'title':title,
            'form':esxiAddForm,
            'error_message': "",
        }
    )

@login_required
def esxiupdate(request):
    c = {}
    c.update(csrf(request))
    if request.method == "POST":
        esxiUpdateForm = ESXiEditForm(request.POST)
        if esxiUpdateForm.is_valid():
            try:
                esxihost = request.POST['hostIP']
                esxi = ESXi.objects.get(esxiIP=str(esxihost))
                esxi.username = request.POST['username']
                esxi.password = request.POST['password']
                esxi.save()
                message = "Success to update ESXi {} information".format(esxihost)
                print message
                return HttpResponseRedirect('../esxi', c)
            except Exception, e:
                message = "Fail to update ESXi {} information. Fail reason: {}".format(esxihost, e)
                # esxiHome = ESXi.objects.all()
                assert isinstance(request, HttpRequest)
                return render(
                    request,
                        '../templates/esxi/esxiedit.html',
                        {
                            'title':title,
                            'form':esxiUpdateForm,
                            'esxiIP': esxihost,
                            'message': message,
                        }
                    )
    else:
        esxiHost = request.GET.get('esxiip')
        esxi = ESXi.objects.get(esxiIP=str(esxiHost))
        username = esxi.username
        password = esxi.password
        assert isinstance(request, HttpRequest)
        return render(
            request,
            '../templates/esxi/esxiedit.html',
            context_instance = RequestContext(request,
            {
                'title':title,
                'esxiIP': esxiHost,
                'username': username,
                'password': password,
                'form': "",
            })
        )

@login_required
def esxidelete(request):
    esxiHost = request.GET.get('esxiip')

    esxi = ESXi.objects.get(esxiIP=str(esxiHost))
    esxi.delete()
    esxiHome = ESXi.objects.all()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        '../templates/esxi/esxiview.html',
        context_instance = RequestContext(request,
        {
            'title':title,
            'esxiHosts':esxiHome,
        })
    )
