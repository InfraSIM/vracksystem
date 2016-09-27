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
from django.contrib.auth.decorators import login_required

@login_required
def vrackdeploy(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        '../templates/vrackdeploy/vrackdeploy.html',
        {
            'message':'vRack System: vRack Deployment',
            'title':"vRackSystem",
            'year':datetime.now().year,
        }
    )
