'''
*********************************************************
Copyright @ 2015 EMC Corporation All Rights Reserved
*********************************************************
'''

import sys, json

from django.contrib.auth.models import User, Group
from django.http import HttpResponse

from AutoDeployUI.models import ESXi
from AutoDeployUI.serializers import ESXiSerializer, UserSerializer, GroupSerializer, NodeDeploySerializer
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status

sys.path.append("../../")
import lib.vRackBuilder.api as vRackBuilder

class ESXiList(generics.ListCreateAPIView):
    """
    List all the ESXi, or create a new ESXi.
    """
    lookup_field = 'id'
    queryset = ESXi.objects.all()
    serializer_class = ESXiSerializer

class ESXiDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a ESXi instance.
    """
    lookup_field = 'id'
    queryset = ESXi.objects.all()
    serializer_class = ESXiSerializer

@api_view(('GET',))
def esxi_datastore(request, id, format=None):
    """
    Get the datastore information of a specific ESXi.
    """
    try:
        esxi = ESXi.objects.get(id=id)
    except ESXi.DoesNotExist:
        content = "Cannot find the ESXi"
        return HttpResponse(content, status=status.HTTP_404_NOT_FOUND)

    usr = esxi.username
    pwd = esxi.password
    host = esxi.esxiIP
    datastore = vRackBuilder.esxi_get_datastores(host, usr, pwd)
    if "fail" in datastore.lower():
        return Response("Cannot get the Datastore information", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(datastore, status=status.HTTP_200_OK)

@api_view(('GET',))
def esxi_network(request, id, format=None):
    """
    Get the network information of a specific ESXi.
    """
    try:
        esxi = ESXi.objects.get(id=id)
    except ESXi.DoesNotExist:
        content = "Cannot find the ESXi"
        return HttpResponse(content, status=status.HTTP_404_NOT_FOUND)

    usr = esxi.username
    pwd = esxi.password
    host = esxi.esxiIP
    network = vRackBuilder.esxi_get_network(host, usr, pwd)
    if "fail" in network.lower():
        return Response("Cannot get the Network information", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(network, status=status.HTTP_200_OK)


@api_view(('POST',))
def esxi_change_memory(request, id, format=None):
    """
    Change VM Memory
    ---
    parameters:
       - name: name
         description: Please input VM name
         required: true
         type: string
         paramType: form
       - name: size
         description: Please input memory size(MB)
         required: true
         type: string
         paramType: form
    """
    try:
        esxi = ESXi.objects.get(id = id)
    except ESXi.DoesNotExist:
        content = "Cannot find the ESXi."
        return HttpResponse(content, status = status.HTTP_404_NOT_FOUND)

    usr = esxi.username
    pwd = esxi.password
    host = esxi.esxiIP

    content = vRackBuilder.esxi_change_memory(host, usr, pwd, request.data["name"], request.data["size"])
    if "fail" in content.lower() or "can't" in content.lower():
        return Response("Fail to Change VM memory size, please check your VM or ESXi", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(content, status=status.HTTP_200_OK)


@api_view(('POST',))
def esxi_add_drive(request, id, format=None):
    """
    Add customized Virtual Disk File
    ---
    parameters:
        - name: name
          description: Please input VM name
          required: true
          type: string
          paramType: form
        - name: size
          description: Please input disk size(G)
          required: true
          type: string
          paramType: form
    """
    try:
        esxi = ESXi.objects.get(id = id)
    except ESXi.DoesNotExist:
        content = "Cannot find the ESXi."
        return HttpResponse(content, status = status.HTTP_404_NOT_FOUND)

    usr = esxi.username
    pwd = esxi.password
    host = esxi.esxiIP

    content = vRackBuilder.esxi_add_drive(host, usr, pwd, request.data["name"], request.data["size"])
    if "fail" in content.lower() or "can't" in content.lower():
        return Response("Fail to add drive, please check your VM or ESXi", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response("Add Drive successfully.", status=status.HTTP_200_OK)

@api_view(('POST', ))
def esxi_add_nic(request, id, format=None):
    """
    Add Virtual Nic to VM
    ---
    parameters:
        - name: name
          description: Please input VM Name
          required: true
          type: string
          paramType: form
        - name: network
          description: Please input Network Name
          required: true
          type: string
          paramType: form
    """
    try:
        esxi = ESXi.objects.get(id = id)
    except ESXi.DoesNotExist:
        content = "Cannot find the ESXi."
        return HttpResponse(content, status = status.HTTP_404_NOT_FOUND)

    usr = esxi.username
    pwd = esxi.password
    host = esxi.esxiIP
    content = vRackBuilder.esxi_add_nic(host, usr, pwd, request.data["name"], request.data["network"])

    if "fail" in content.lower() or "can't" in content.lower():
        return Response("Fail to add NIC, please check your VM or ESXi", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response("Add NIC successfully.", status=status.HTTP_200_OK)

@api_view(('POST',))
def esxi_deploy(request, id, format=None):
    """
    Deploy virtual nodes to a specific ESXi.
    OVA file name is optional
    ---
    parameters:
        - name: datastore
          description: Please input one datastore name (Datastore00)
          required: true
          type: string
          paramType: form
        - name: power
          description: VM status after deployed (on|off)
          required: true
          type: string
          paramType: form
        - name: duration
          description: Please input the interval between two nodes deployment.
          required: true
          type: string
          paramType: form
        - name: controlnetwork
          description: Please input the control network. This not works in PDU deployment.
          required: true
          type: string
          paramType: form
        - name: nodetype
          description: vNode type (vnode|vpdu)
          required: true
          type: string
          paramType: form
        - name: count
          description: Please input the node count that to be deployed.
          required: true
          type: string
          paramType: form
        - name: ova
          description: OVA file name
          required: false
          type: string
          paramType: form
    """
    try:
        esxi = ESXi.objects.get(id=id)
    except ESXi.DoesNotExist:
        content = "Cannot find the ESXi."
        return HttpResponse(content, status = status.HTTP_404_NOT_FOUND)

    usr = esxi.username
    pwd = esxi.password
    host = esxi.esxiIP

    if request.data.has_key("ova"):
        return Response(vRackBuilder.singleDeploy(host, usr, pwd, request.data['datastore'], request.data['power'], request.data['duration'], request.data['controlnetwork'], request.data['nodetype'], request.data['count'], img = request.data['ova']), status=status.HTTP_200_OK);

    return Response(vRackBuilder.singleDeploy(host, usr, pwd, request.data['datastore'], request.data['power'], request.data['duration'], request.data['controlnetwork'], request.data['nodetype'], request.data['count']), status=status.HTTP_200_OK);

@api_view(('POST',))
def list_ova(request, format=None):
    """
    List the ova on the server.
    ---
    parameters:
        - name: type
          description: Please input the OVA type
          required: true
          type: string
          paramType: form
    """
    return Response(vRackBuilder.listOva(request.data["type"]), status=status.HTTP_200_OK)

@api_view(('POST',))
def upload_ova(request, format=None):
    """
    Upload OVA file
    """
    try:
        return Response(vRackBuilder.uploadOva(request.FILES['file'], request.data["filetype"]), status=status.HTTP_200_OK)
    except:
        return Response(json.dumps("failed"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(('POST',))
def esxi_vpdu_host_config_list(request, id, format=None):
    """
    List vPDU ESXi host configuration Information
    ---
    parameters:
        - name: ip
          description: vPDU IP address
          required: true
          type: string
          paramType: form
    """
    try:
        esxi = ESXi.objects.get(id=id)
    except ESXi.DoesNotExist:
        content = "Cannot find the ESXi."
        return HttpResponse(content, status = status.HTTP_404_NOT_FOUND)

    vpdu_host_list = json.loads(vRackBuilder.vpdu_list_esxi_config_info(request.data["ip"]))
    if len(vpdu_host_list[0]) == 3:
        vpdu_host_list[0].insert(0, str(ESXi.objects.get(esxiIP=vpdu_host_list[0][0]).id))

    return Response(json.dumps(vpdu_host_list), status=status.HTTP_200_OK)

@api_view(('POST', ))
def esxi_vpdu_set_pdu_info(request, id, format=None):
    """
    Set PDU information including name, database, and MIB data dir
    ---
    parameters:
        - name: ip
          description: PDU ip address
          required: true
          type: string
          paramType: form
        - name: name
          description: PDU name
          required: true
          type: string
          paramType: form
        - name: database
          description: PDU database file
          required: true
          type: string
          paramType: form
        - name: snmpdata
          description: MIB data directory
          required: true
          paramType: form
    """
    try:
        esxi = ESXi.objects.get(id=id)
    except ESXi.DoesNotExist:
        content = "Cannot find the ESXi."
        return HttpResponse(content, status=status.HTTP_404_NOT_FOUND)

    content = vRackBuilder.vpdu_set_pdu_info(request.data['ip'],
                                             request.data['name'],
                                             request.data['database'],
                                             request.data['snmpdata'])

    if content == None:
        return Response("Fail to set the PDU information", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(content, status=status.HTTP_200_OK)

@api_view(('POST',))
def esxi_vpdu_host_config_add(request, id, format=None):
    """
    Add vPDU ESXi host configuration Information
    ---
    parameters:
        - name: ip
          description: vPDU IP address
          required: true
          type: string
          paramType: form
    """
    try:
        esxi = ESXi.objects.get(id=id)
    except ESXi.DoesNotExist:
        content = "Cannot find the ESXi."
        return HttpResponse(content, status = status.HTTP_404_NOT_FOUND)

    content = vRackBuilder.vpdu_add_esxi_config_info(request.data["ip"], esxi.esxiIP, esxi.username, esxi.password)
    if "success" in content.lower():
        return Response(content, status=status.HTTP_200_OK)
    else:
        return Response("Fail to set the PDU ESXi host information.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(('POST',))
def esxi_vpdu_host_config_del(request, id, format=None):
    """
    Delete vPDU ESXi host configuration Information
    ---
    parameters:
        - name: ip
          description: vPDU IP address
          required: true
          type: string
          paramType: form
    """
    try:
        esxi = ESXi.objects.get(id=id)
    except ESXi.DoesNotExist:
        content = "Cannot find the ESXi."
        return HttpResponse(content, status = status.HTTP_404_NOT_FOUND)

    content = vRackBuilder.vpdu_delete_esxi_config_info(request.data["ip"])
    if "success" in content.lower():
        return Response(content, status=status.HTTP_200_OK)
    else:
        return Response("Fail to delete the PDU ESXi host information.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(('POST',))
def esxi_vpdu_map_list(request, id, format = None):
    """
    List vPDU <-> vNode mapping Information
    ---
    parameters:
        - name: ip
          description: vPDU IP address
          required: true
          type: string
          paramType: form
    """
    try:
        esxi = ESXi.objects.get(id=id)
    except ESXi.DoesNotExist:
        content = "Cannot find the ESXi."
        return HttpResponse(content, status = status.HTTP_404_NOT_FOUND)

    content = vRackBuilder.vpdu_map_list(request.data["ip"])
    return Response(content, status=status.HTTP_200_OK)

@api_view(('POST',))
def esxi_vpdu_pwd_list(request, id, format = None):
    """
    List vPDU Passowrd<-> vNode Password Information
    ---
    parameters:
        - name: ip
          description: vPDU IP address
          required: true
          type: string
          paramType: form
        - name: pdu
          description: PDU Number(1-6)
          required: true
          type: string
          paramType: form
    """
    try:
        esxi = ESXi.objects.get(id=id)
    except ESXi.DoesNotExist:
        content = "Cannot find the ESXi."
        return HttpResponse(content, status = status.HTTP_404_NOT_FOUND)

    content = vRackBuilder.vpdu_pwd_list(request.data["ip"], request.data["pdu"])
    return Response(content, status=status.HTTP_200_OK)

@api_view(('POST',))
def esxi_vpdu_restart(request, id, format = None):
    """
    vPDU restart
    ---
    parameters:
        - name: ip
          description: vPDU IP address
          required: true
          type: string
          paramType: form
    """
    try:
        esxi = ESXi.objects.get(id=id)
    except ESXi.DoesNotExist:
        content = "Cannot find the ESXi."
        return HttpResponse(content, status = status.HTTP_404_NOT_FOUND)

    content = vRackBuilder.vpdu_restart(request.data["ip"])
    if "success" in content.lower():
        return Response(content, status=status.HTTP_200_OK)
    else:
        return Response("Fail to restart the PDU.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(('POST',))
def esxi_vpdu_map_add(request, id, format = None):
    """
    Add vPDU <-> vNode mapping Information
    ---
    parameters:
        - name: ip
          description: vPDU IP address
          required: true
          type: string
          paramType: form
        - name: dt
          description: vNode datastore
          required: true
          type: string
          paramType: form
        - name: name
          description: vNode name
          required: true
          type: string
          paramType: form
        - name: pdu
          description: PDU Number(1-6)
          required: true
          type: string
          paramType: form
        - name: port
          description: PDU Port Number(1-24)
          required: true
          type: string
          paramType: form
    """
    try:
        esxi = ESXi.objects.get(id=id)
    except ESXi.DoesNotExist:
        content = "Cannot find the ESXi."
        return HttpResponse(content, status = status.HTTP_404_NOT_FOUND)

    content = vRackBuilder.vpdu_map_add(request.data["ip"], request.data['dt'], request.data['name'], request.data['pdu'], request.data['port'])
    if "success" in content.lower():
        return Response(content, status=status.HTTP_200_OK)
    else:
        return Response("Fail to add the pdu mapping.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(('POST',))
def esxi_vpdu_map_update(request, id, format = None):
    """
    Update vPDU <-> vNode mapping Information
    ---
    parameters:
        - name: ip
          description: vPDU IP address
          required: true
          type: string
          paramType: form
        - name: dt
          description: vNode datastore
          required: true
          type: string
          paramType: form
        - name: name
          description: vNode name
          required: true
          type: string
          paramType: form
        - name: pdu
          description: PDU Number(1-6)
          required: true
          type: string
          paramType: form
        - name: port
          description: PDU Port Number(1-24)
          required: true
          type: string
          paramType: form
    """
    try:
        esxi = ESXi.objects.get(id=id)
    except ESXi.DoesNotExist:
        content = "Cannot find the ESXi."
        return HttpResponse(content, status = status.HTTP_404_NOT_FOUND)

    content = vRackBuilder.vpdu_map_update(request.data["ip"], request.data['dt'], request.data['name'], request.data['pdu'], request.data['port'])
    if "success" in content.lower():
        return Response(content, status=status.HTTP_200_OK)
    else:
        return Response("Fail to update the pdu mapping.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(('POST',))
def esxi_vpdu_map_delete(request, id, format = None):
    """
    Delete vPDU <-> vNode mapping Information
    ---
    parameters:
        - name: ip
          description: vPDU IP address
          required: true
          type: string
          paramType: form
        - name: dt
          description: vNode datastore
          required: true
          type: string
          paramType: form
        - name: name
          description: vNode name
          required: true
          type: string
          paramType: form
    """
    try:
        esxi = ESXi.objects.get(id=id)
    except ESXi.DoesNotExist:
        content = "Cannot find the ESXi."
        return HttpResponse(content, status = status.HTTP_404_NOT_FOUND)

    content = vRackBuilder.vpdu_map_delete(request.data["ip"], request.data['dt'], request.data['name'])
    if "success" in content.lower():
        return Response(content, status=status.HTTP_200_OK)
    else:
        return Response("Fail to delete the pdu mapping.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(('POST',))
def esxi_vpdu_pwd_add(request, id, format = None):
    """
    Add vPDU Password <-> vNode Password Information
    ---
    parameters:
        - name: ip
          description: vPDU IP address
          required: true
          type: string
          paramType: form
        - name: pdu
          description: PDU Number(1-6)
          required: true
          type: string
          paramType: form
        - name: port
          description: PDU Port Number(1-24)
          required: true
          type: string
          paramType: form
        - name: password
          description: PDU Port Password
          required: true
          paramType: form
    """
    try:
        esxi = ESXi.objects.get(id=id)
    except ESXi.DoesNotExist:
        content = "Cannot find the ESXi."
        return HttpResponse(content, status = status.HTTP_404_NOT_FOUND)

    content = vRackBuilder.vpdu_pwd_add(request.data["ip"], request.data['pdu'], request.data['port'], request.data['password'])
    if "success" in content.lower():
        return Response(content, status=status.HTTP_200_OK)
    else:
        return Response("Fail to add the vpdu password.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(('GET',))
def esxi_get_all_vms(request, id, format=None):
    """
    List VMs in ESXi Host
    """
    try:
        esxi = ESXi.objects.get(id=id)
    except ESXi.DoesNotExist:
        content = "Cannot find the ESXi."
        return HttpResponse(content, status = status.HTTP_404_NOT_FOUND)

    usr = esxi.username
    pwd = esxi.password
    host = esxi.esxiIP

    content = vRackBuilder.get_all_vms(host, usr, pwd)

    if "fail" in content.lower():
        return Response("Cannot get the vm list information", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(content, status=status.HTTP_200_OK)

@api_view(('POST',))
def esxi_get_vm_info(request, id, format=None):
    """
    GET VM Detailed information
    ---
    parameters:
        - name: name
          description: vNode Name
          required: true
          type: string
          paramType: form
    """
    try:
        esxi = ESXi.objects.get(id=id)
    except ESXi.DoesNotExist:
        content = "Cannot find the ESXi."
        return HttpResponse(content, status = status.HTTP_404_NOT_FOUND)

    usr = esxi.username
    pwd = esxi.password
    host = esxi.esxiIP

    content = vRackBuilder.get_vm_info(host, usr, pwd, request.data["name"])

    if "fail" in content.lower() or "can't" in content.lower():
        return Response("Fail to get the VM information. Please check.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(content, status=status.HTTP_200_OK)

@api_view(('POST',))
def esxi_poweron_vm(request, id, format=None):
    """
    Power On VM in ESXi Host
    ---
    parameters:
        - name: name
          description: vNode Name
          required: true
          type: string
          paramType: form
    """
    try:
        esxi = ESXi.objects.get(id=id)
    except ESXi.DoesNotExist:
        content = "Cannot find the ESXi."
        return HttpResponse(content, status = status.HTTP_404_NOT_FOUND)

    usr = esxi.username
    pwd = esxi.password
    host = esxi.esxiIP

    content = vRackBuilder.esxi_poweron_vm(host, usr, pwd, request.data['name'])
    if "fail" in content.lower() or "can't" in content.lower():
        return Response("Fail to power on the VM. Please check.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(content, status=status.HTTP_200_OK)

@api_view(('POST',))
def esxi_poweroff_vm(request, id, format=None):
    """
    Power off VM in ESXi Host
    ---
    parameters:
        - name: name
          description: vNode Name
          required: true
          type: string
          paramType: form
    """
    try:
        esxi = ESXi.objects.get(id=id)
    except ESXi.DoesNotExist:
        content = "Cannot find the ESXi."
        return HttpResponse(content, status = status.HTTP_404_NOT_FOUND)

    usr = esxi.username
    pwd = esxi.password
    host = esxi.esxiIP

    content = vRackBuilder.esxi_poweroff_vm(host, usr, pwd, request.data['name'])
    if "fail" in content.lower() or "can't" in content.lower():
        return Response("Fail to power off the VM. Please check.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(content, status=status.HTTP_200_OK)

@api_view(('POST',))
def esxi_reset_vm(request, id, format=None):
    """
    Reset VM in ESXi Host
    ---
    parameters:
        - name: name
          description: vNode Name
          required: true
          type: string
          paramType: form
    """
    try:
        esxi = ESXi.objects.get(id=id)
    except ESXi.DoesNotExist:
        content = "Cannot find the ESXi."
        return HttpResponse(content, status = status.HTTP_404_NOT_FOUND)

    usr = esxi.username
    pwd = esxi.password
    host = esxi.esxiIP

    content = vRackBuilder.esxi_reset_vm(host, usr, pwd, request.data['name'])
    if "fail" in content.lower() or "can't" in content.lower():
        return Response("Fail to reset the VM. Please check.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(content, status=status.HTTP_200_OK)

@api_view(('POST',))
def esxi_destroy_vm(request, id, format=None):
    """
    Destroy VM in ESXi Host
    ---
    parameters:
        - name: name
          description: vNode Name
          required: true
          type: string
          paramType: form
    """
    try:
        esxi = ESXi.objects.get(id=id)
    except ESXi.DoesNotExist:
        content = "Cannot find the ESXi."
        return HttpResponse(content, status = status.HTTP_404_NOT_FOUND)

    usr = esxi.username
    pwd = esxi.password
    host = esxi.esxiIP

    content = vRackBuilder.esxi_destory_vm(host, usr, pwd, request.data['name'])
    if "fail" in content.lower() or "can't" in content.lower():
        return Response("Fail to destroy the VM. Please check.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(content, status=status.HTTP_200_OK)

@api_view(('GET',))
def esxi_list_hardware(request, id, format=None):
    """
    List ESXi Host Hardware Info
    """
    try:
        esxi = ESXi.objects.get(id=id)
    except ESXi.DoesNotExist:
        content = "Cannot find the ESXi."
        return HttpResponse(content, status = status.HTTP_404_NOT_FOUND)

    usr = esxi.username
    pwd = esxi.password
    host = esxi.esxiIP

    content = vRackBuilder.esxi_list_hardware(host, usr, pwd)
    if "fail" in content.lower():
        return Response("Fail to get the hardware information.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(content, status=status.HTTP_200_OK)
