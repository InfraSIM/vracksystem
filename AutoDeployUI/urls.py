'''
*********************************************************
Copyright @ 2015 EMC Corporation All Rights Reserved
*********************************************************
'''

"""AutoDeployUI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from datetime import datetime

from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from app.view import views

from django.contrib import admin
from app.module.forms import BootstrapAuthenticationForm

urlpatterns = [
    ################################### Rest APIs ###############################################
    url(r'^api/v1/esxi/$', views.ESXiList.as_view(), name="esxi_list"),
    url(r'^api/v1/esxi/(?P<id>[0-9]+)/$', views.ESXiDetail.as_view(), name="esxi_detail"),
    url(r'^api/v1/esxi/(?P<id>[0-9]+)/getvms$', 'app.view.views.esxi_get_all_vms', name='esxi_get_all_vms'),
    url(r'^api/v1/esxi/(?P<id>[0-9]+)/getvminfo$', 'app.view.views.esxi_get_vm_info', name='esxi_get_vm_info'),
    url(r'^api/v1/esxi/(?P<id>[0-9]+)/poweronvm$', 'app.view.views.esxi_poweron_vm', name='esxi_poweron_vm'),
    url(r'^api/v1/esxi/(?P<id>[0-9]+)/poweroffvm$', 'app.view.views.esxi_poweroff_vm', name='esxi_poweroff_vm'),
    url(r'^api/v1/esxi/(?P<id>[0-9]+)/resetvm$', 'app.view.views.esxi_reset_vm', name='esxi_reset_vm'),
    url(r'^api/v1/esxi/(?P<id>[0-9]+)/destroyvm$', 'app.view.views.esxi_destroy_vm', name='esxi_destroy_vm'),
    url(r'^api/v1/esxi/(?P<id>[0-9]+)/hardware$', 'app.view.views.esxi_list_hardware', name='esxi_list_hardware'),
    url(r'^api/v1/esxi/(?P<id>[0-9]+)/datastores$', 'app.view.views.esxi_datastore', name='esxi_get_datastore'),
    url(r'^api/v1/esxi/(?P<id>[0-9]+)/networks$', 'app.view.views.esxi_network', name='esxi_get_network'),
    url(r'^api/v1/esxi/(?P<id>[0-9]+)/deploy$', 'app.view.views.esxi_deploy', name='esxi_deploy'),
    url(r'^api/v1/esxi/(?P<id>[0-9]+)/adddrive$', 'app.view.views.esxi_add_drive', name='esxi_add_drive'),
    url(r'^api/v1/esxi/(?P<id>[0-9]+)/addnic$', 'app.view.views.esxi_add_nic', name='esxi_add_nic'),
    url(r'^api/v1/esxi/(?P<id>[0-9]+)/vpduhostlist$', 'app.view.views.esxi_vpdu_host_config_list', name='esxi_vpdu_host_config_list'),
    url(r'^api/v1/esxi/(?P<id>[0-9]+)/vpdusetpduinfo$', 'app.view.views.esxi_vpdu_set_pdu_info', name='esxi_vpdu_set_pdu_info'),
    url(r'^api/v1/esxi/(?P<id>[0-9]+)/vpduhostadd$', 'app.view.views.esxi_vpdu_host_config_add', name='esxi_vpdu_host_config_add'),
    url(r'^api/v1/esxi/(?P<id>[0-9]+)/vpduhostdel$', 'app.view.views.esxi_vpdu_host_config_del', name='esxi_vpdu_host_config_del'),
    url(r'^api/v1/esxi/(?P<id>[0-9]+)/vpdumapadd$', 'app.view.views.esxi_vpdu_map_add', name='esxi_vpdu_map_add'),
    url(r'^api/v1/esxi/(?P<id>[0-9]+)/vpdumapupdate$', 'app.view.views.esxi_vpdu_map_update', name='esxi_vpdu_map_update'),
    url(r'^api/v1/esxi/(?P<id>[0-9]+)/vpdumaplist$', 'app.view.views.esxi_vpdu_map_list', name='esxi_vpdu_map_list'),
    url(r'^api/v1/esxi/(?P<id>[0-9]+)/vpdumapdelete$', 'app.view.views.esxi_vpdu_map_delete', name='esxi_vpdu_map_delete'),
    url(r'^api/v1/esxi/(?P<id>[0-9]+)/vpdupwdadd$', 'app.view.views.esxi_vpdu_pwd_add', name='esxi_vpdu_pwd_add'),
    url(r'^api/v1/esxi/(?P<id>[0-9]+)/vpdupwdlist$', 'app.view.views.esxi_vpdu_pwd_list', name='esxi_vpdu_pwd_list'),
    url(r'^api/v1/esxi/(?P<id>[0-9]+)/vpdurestart$', 'app.view.views.esxi_vpdu_restart', name='esxi_vpdu_restart'),

    # url(r'^api/v1/users/$', views.UserList.as_view(), name="user_list"),
    # url(r'^api/v1/users/(?P<id>[0-9]+)/$', views.UserDetail.as_view(), name="user_detail"),
    # url(r'^api/v1/groups/$', views.GroupList.as_view(), name="group_list"),
    # url(r'^api/v1/groups/(?P<id>[0-9]+)/$', views.GroupDetail.as_view(), name="group_detail"),

    url(r'^api-auth/', include('rest_framework.urls',namespace='rest_framework')),

    url(r'^api/v1/ova/list$', 'app.view.views.list_ova', name='listova'),
    url(r'^api/v1/ova/upload$', 'app.view.views.upload_ova', name='uploadova'),

    ################################### Web Pages ###############################################
    # Home page:
    url(r'^home/$', 'app.view.index.home', name='home'),
    url(r'^$', 'app.view.index.index', name='index'),

    # ESXi related pages:
    url(r'^esxi$', 'app.view.esxi.esxi', name='esxi'),
    url(r'^esxi/add$', 'app.view.esxi.esxiadd', name='esxiadd'),
    url(r'^esxi/update$', 'app.view.esxi.esxiupdate', name='esxiupdate'),
    url(r'^esxi/delete$', 'app.view.esxi.esxidelete', name='esxidelete'),
    # url(r'^esxi/deploy$', 'app.view.esxi.esxideploy', name='esxideploy'),

    # KVM page
    url(r'^kvm$', 'app.view.kvm.kvm', name='kvm'),

    # Docker page
    url(r'^docker$', 'app.view.docker.docker', name='docker'),

    # vNode Deploy
    url(r'^vnode/deploy$', 'app.view.vnode.vnodedeploy', name='vnodedeploy'),
    url(r'^vnode/control$', 'app.view.vnode.vnodecontrol', name='vnodecontrol'),
    url(r'^vnode/uploadova', 'app.view.vnode.uploadova', name='uploadova'),

    # vPDU
    url(r'^vpdu/basic$', 'app.view.vpdu.getbasic', name='vpdubasic'),
    url(r'^vpdu/esxihost$', 'app.view.vpdu.getesxihost', name='vpduesxi'),
    url(r'^vpdu/password$', 'app.view.vpdu.getpassword', name='vpdupassword'),
    url(r'^vpdu/mapping$', 'app.view.vpdu.getmapping', name='vpdumapping'),

    # vRack Builder
    url(r'^vrackdeploy$', 'app.view.vrackdeploy.vrackdeploy', name='vrackdeploy'),

    # vNode Customization
    url(r'^vnodecustom/adddrive$', 'app.view.vnodecustom.adddrive', name='adddrive'),
    url(r'^vnodecustom/addnic$', 'app.view.vnodecustom.addnic', name='addnic'),

    # Support Page
    url(r'^support$', 'app.view.support.support', name='support'),

    url(r'^login/$',
        'django.contrib.auth.views.login',
        {
            'template_name': 'app/login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
                {
                    'title': 'Log in',
                    'year': datetime.now().year,
                }
        },
        name='login'),
    url(r'^logout$',
        'django.contrib.auth.views.logout',
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^docs/', include('rest_framework_swagger.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
