'''
*********************************************************
Copyright @ 2015 EMC Corporation All Rights Reserved
*********************************************************
'''

from django import forms

class ESXiAddForm(forms.Form):
    esxihost = forms.GenericIPAddressField(required=True, initial="10.62.59.18")
    username = forms.CharField(max_length=20, required=True, initial="root")
    password = forms.CharField(widget=forms.PasswordInput, required=True, initial="1234567")

class ESXiEditForm(forms.Form):
    username = forms.CharField(max_length=20, required=True, initial="root")
    password = forms.CharField(widget=forms.PasswordInput, required=True, initial="1234567")

class NodeDeployForm(forms.Form):
    duration = forms.IntegerField(min_value=0, required=True, initial=0)
    nodeCount = forms.IntegerField(min_value=1, required=True, initial=1)
