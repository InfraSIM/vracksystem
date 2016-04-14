'''
*********************************************************
Copyright @ 2015 EMC Corporation All Rights Reserved
*********************************************************
'''

from django.db import models

class ESXi(models.Model):
    esxiIP = models.GenericIPAddressField(max_length=32, unique=True)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)

    class Meta:
        ordering = ["id"]

    def __unicode__(self):
        return u'%s %s %s' % (self.esxiIP, self.username, self.password)