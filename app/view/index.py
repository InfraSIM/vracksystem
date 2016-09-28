'''
*********************************************************
Copyright @ 2015 EMC Corporation All Rights Reserved
*********************************************************
'''

"""
Definition of views.
"""

from datetime import datetime

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required

from django.http import HttpRequest
from django.template import RequestContext

def main(request):
  if request.user.is_authenticated():
    return redirect(reverse_lazy('home'))
  else:
    return redirect(reverse_lazy('login'))

@login_required
def home(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        context = 
        {
            'username':request.user.username,
            'message':'vRack System: Get OVA, Deploy virtual nodes, Manage virtual nodes. virtual PDU function is in development.',
            'title':"vRack System",
            'year':'2016',
        }
    )
