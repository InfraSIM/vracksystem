'''
*********************************************************
Copyright @ 2015 EMC Corporation All Rights Reserved
*********************************************************
'''

__author__ = 'wuy1'
import datetime

from rest_framework import serializers
from django.contrib.auth.models import User, Group
from AutoDeployUI.models import ESXi

class ESXiSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ESXi
        fields = ('id', 'esxiIP', 'username', 'password')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_staff', 'is_superuser','is_active', 'last_login')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')

class NodeDeploySerializer(serializers.Serializer):
        datastore = serializers.CharField()
        power = serializers.CharField()
        type = serializers.CharField()
        duration = serializers.CharField()
        count = serializers.CharField()