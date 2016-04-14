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

def kvm(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        '../templates/kvm/kvm.html',
        context_instance = RequestContext(request,
        {
            'message':'vRack System: KVM Resource',
            'title':"vRackSystem",
            'year':datetime.now().year,
        })
    )