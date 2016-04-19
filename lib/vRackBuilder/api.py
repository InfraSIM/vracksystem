'''
*********************************************************
Copyright @ 2015 EMC Corporation All Rights Reserved
*********************************************************
'''

import os
import json
import time
import operator
import socket
from configobj import ConfigObj
import pexpect
import datetime

import paramiko
from routines import *
from pyVim import connect
from pyVmomi import vim
import tasks

IMAGE_PATH = 'ova/'
URL_LINK = 'https://gpsbuildfarm.corp.emc.com/view/HW_Simulation/job/HW_Simulation_%s/%s/artifact/ova_artifact/%s'

def esxi_get_datastores(host, usr, pwd):
    """ Get all datastore information of 1 ESXi. """
    try:
        si = connect.Connect(host=host, user=usr, pwd=pwd)

        datacenter_obj = si.content.rootFolder.childEntity[0]
        datastore_list = datacenter_obj.datastoreFolder.childEntity
        dt_list = []
        for dt in datastore_list:
            dt_list.append(dt.name)
        connect.Disconnect(si)
    except Exception, e:
        return "Get Datastore Failed!"

    return json.dumps(dt_list)

def esxi_get_network(host, usr, pwd):
    """ Get the Network information of 1 ESXi. """
    network_list = []
    try:
        si = connect.Connect(host=host, user=usr, pwd=pwd)
        views = si.content.viewManager.CreateContainerView(si.content.rootFolder, [vim.Network], True)
        for view in views.view:
            network_list.append(view.name)
        connect.Disconnect(si)
    except Exception, e:
        return "Get Network failed!"

    return json.dumps(network_list)

def esxi_list_hardware(host, usr, pwd):
    try:
        si = connect.Connect(host=host, user=usr, pwd=pwd)
        host_view = si.content.viewManager.CreateContainerView(si.content.rootFolder, [vim.HostSystem], True)
        info={"cores":host_view.view[0].hardware.cpuInfo.numCpuCores,
                        "freq":host_view.view[0].hardware.cpuInfo.hz,
                        "threads":host_view.view[0].hardware.cpuInfo.numCpuThreads,
                        "memory":host_view.view[0].hardware.memorySize}
        connect.Disconnect(si)
    except Exception, e:
        return "Get ESXi Hardware Info Failed!"

    return json.dumps(info)

def get_all_vms(host, usr, pwd):
    vms_list = []
    try:
        si = connect.Connect(host=host, user=usr, pwd=pwd)
        vm_view = si.content.viewManager.CreateContainerView(si.content.rootFolder, [vim.VirtualMachine], True)
        for vm in vm_view.view:
           summary = vm.summary
           dt = summary.config.vmPathName.split(" ")[0]
           dt = dt[1:(len(dt) - 1)]
           vm_config = {"name":summary.config.name, "datastore":dt,"status":summary.runtime.powerState[7:],
                          "ip":[], "uuid":summary.config.instanceUuid}
           if len(vm.guest.net) > 0:
               for nic in vm.guest.net:
                   if len(nic.ipAddress) == 0:
                       continue
                   elif len(nic.ipAddress[0]) > 15:
                       pass
                   else:
                       vm_config["ip"].append(nic.ipAddress[0])
           vms_list.append(vm_config)
        connect.Disconnect(si)
    except Exception, e:
        return "Get vms failed!"
    return json.dumps(vms_list)

def get_vm_info(host, usr, pwd, vm_name):
    try:
        si = connect.Connect(host=host, user=usr, pwd=pwd)
        vm_view = si.content.viewManager.CreateContainerView(si.content.rootFolder, [vim.VirtualMachine], True)
        uuid = ""
        for vm in vm_view.view:
            if vm.summary.config.name == vm_name:
                uuid = vm.summary.config.instanceUuid
                break
        if uuid == "":
            connect.Disconnect(si)
            return "Can't find VM(%s)!" % vm_name

        vm = si.content.searchIndex.FindByUuid(None, uuid, True, True)
        vm_details = {"cpu":vm.config.hardware.numCPU, "memory":vm.config.hardware.memoryMB, "drive":[], "network":[]}
        for device in vm.config.hardware.device:
            if device.backing is not None:
                if device.deviceInfo.label.find("disk") > 0:
                    vm_details["drive"].append(device.deviceInfo.label)
                elif device.deviceInfo.label.find("adapter") > 0:
                    vm_details["network"].append(device.deviceInfo.label)
                else:
                    pass
        connect.Disconnect(si)
    except Exception, e:
        return "Get VM(%s) details failed!" % vm_name

    return json.dumps(vm_details)

def esxi_poweron_vm(host, usr, pwd, vm_name):
    try:
        si = connect.Connect(host=host, user=usr, pwd=pwd)
        vm_view = si.content.viewManager.CreateContainerView(si.content.rootFolder, [vim.VirtualMachine], True)
        uuid = ""
        for vm in vm_view.view:
            if vm.summary.config.name == vm_name:
                uuid = vm.summary.config.instanceUuid
                break
        if uuid == "":
            connect.Disconnect(si)
            return "Can't find VM(%s)!" % vm_name

        vm = si.content.searchIndex.FindByUuid(None, uuid, True, True)
        if vm.runtime.powerState == "poweredOn":
            connect.Disconnect(si)
            return "VM(%s) already powered On" % (vm_name)

        task = vm.PowerOnVM_Task()
        tasks.wait_for_tasks(si, [task])
        connect.Disconnect(si)
    except Exception, e:
        return "PowerOn VM(%s) failed!" % vm_name

    return "PowerOn VM(%s) success!" % vm_name

def esxi_poweroff_vm(host, usr, pwd, vm_name):
    try:
        si = connect.Connect(host=host, user=usr, pwd=pwd)
        vm_view = si.content.viewManager.CreateContainerView(si.content.rootFolder, [vim.VirtualMachine], True)
        uuid = ""
        for vm in vm_view.view:
            if vm.summary.config.name == vm_name:
                uuid = vm.summary.config.instanceUuid
                break
        if uuid == "":
            connect.Disconnect(si)
            return "Can't find VM(%s)!" % vm_name

        vm = si.content.searchIndex.FindByUuid(None, uuid, True, True)
        if vm.runtime.powerState == "poweredOff":
            connect.Disconnect(si)
            return "VM(%s) already powered Off" % (vm_name)

        task = vm.PowerOffVM_Task()
        tasks.wait_for_tasks(si, [task])
        connect.Disconnect(si)
    except Exception, e:
        return "PowerOff VM(%s) failed!" % vm_name

    return "PowerOff VM(%s) success!" % vm_name

def esxi_reset_vm(host, usr, pwd, vm_name):
    try:
        si = connect.Connect(host=host, user=usr, pwd=pwd)
        vm_view = si.content.viewManager.CreateContainerView(si.content.rootFolder, [vim.VirtualMachine], True)
        uuid = ""
        for vm in vm_view.view:
            if vm.summary.config.name == vm_name:
                uuid = vm.summary.config.instanceUuid
                break
        if uuid == "":
            connect.Disconnect(si)
            return "Can't find VM(%s)!" % vm_name

        vm = si.content.searchIndex.FindByUuid(None, uuid, True, True)
        task = vm.ResetVM_Task()
        tasks.wait_for_tasks(si, [task])
        connect.Disconnect(si)
    except Exception, e:
        return "Reset VM(%s) failed!" % vm_name

    return "Reset VM(%s) success!" % vm_name


def esxi_destory_vm(host, usr, pwd, vm_name):
    try:
        si = connect.Connect(host=host, user=usr, pwd=pwd)
        vm_view = si.content.viewManager.CreateContainerView(si.content.rootFolder, [vim.VirtualMachine], True)
        uuid = ""
        for vm in vm_view.view:
            if vm.summary.config.name == vm_name:
                uuid = vm.summary.config.instanceUuid
                break
        if uuid == "":
            connect.Disconnect(si)
            return "Can't find VM(%s)!" % vm_name

        vm = si.content.searchIndex.FindByUuid(None, uuid, True, True)
        if vm.runtime.powerState == "poweredOn":
            task = vm.PowerOffVM_Task()
            tasks.wait_for_tasks(si, [task])

        task = vm.Destroy_Task()
        tasks.wait_for_tasks(si, [task])
        connect.Disconnect(si)
    except Exception, e:
        print e
        return "Destory VM(%s) failed!" % vm_name

    return "Destory VM(%s) success!" % vm_name

def esxi_change_memory(host, usr, pwd, vm_name, mem_size):
    try:
        si = connect.Connect(host=host, user=usr, pwd=pwd)
        vm_view = si.content.viewManager.CreateContainerView(si.content.rootFolder, [vim.VirtualMachine], True)
        uuid = ""
        for vm in vm_view.view:
            if vm.summary.config.name == vm_name:
                uuid = vm.summary.config.instanceUuid
                break
        if uuid == "":
            connect.Disconnect(si)
            return "Can't find VM(%s)!" % vm_name

        vm = si.content.searchIndex.FindByUuid(None, uuid, True, True)
        spec = vim.vm.ConfigSpec()
        spec.memoryMB = int(mem_size) + 512
        task = vm.ReconfigVM_Task(spec)
        tasks.wait_for_tasks(si, [task])

        connect.Disconnect(si)
    except Exception, e:
        return "Change VM Memory on VM(%s) failed!" % vm_name
    return "Change VM(%s) Memory successfully!" % vm_name

def esxi_add_drive(host, usr, pwd, vm_name, disk_size):
    try:
        si = connect.Connect(host=host, user=usr, pwd=pwd)
        vm_view = si.content.viewManager.CreateContainerView(si.content.rootFolder, [vim.VirtualMachine], True)
        uuid = ""
        for vm in vm_view.view:
            if vm.summary.config.name == vm_name:
                uuid = vm.summary.config.instanceUuid
                break
        if uuid == "":
            connect.Disconnect(si)
            return "Can't find VM(%s)!" % vm_name
        vm = si.content.searchIndex.FindByUuid(None, uuid, True, True)
        esxi_add_new_disk_process(vm, si, disk_size)
        connect.Disconnect(si)
    except Exception, e:
        return "Create new drive on VM(%s) failed!" % vm_name

    return "Create new drive on VM(%s) successfully!" % vm_name

def esxi_add_new_disk_process(vm, si, disk_size):
        spec = vim.vm.ConfigSpec()
        # get all disks on a VM, set unit_number to the next available
        for dev in vm.config.hardware.device:
            if hasattr(dev.backing, 'fileName'):
                unit_number = int(dev.unitNumber) + 1
                # unit_number 7 reserved for scsi controller
                if unit_number == 7:
                    unit_number += 1
                if unit_number >= 16:
                    print "we don't support this many disks"
                    return
            if isinstance(dev, vim.vm.device.VirtualSCSIController):
                controller = dev
        # add disk here
        dev_changes = []
        new_disk_kb = int(disk_size) * 1024 * 1024
        disk_spec = vim.vm.device.VirtualDeviceSpec()
        disk_spec.fileOperation = "create"
        disk_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
        disk_spec.device = vim.vm.device.VirtualDisk()
        disk_spec.device.backing = \
            vim.vm.device.VirtualDisk.FlatVer2BackingInfo()
        disk_spec.device.backing.thinProvisioned = True
        disk_spec.device.backing.diskMode = 'persistent'
        disk_spec.device.unitNumber = unit_number
        disk_spec.device.capacityInKB = new_disk_kb
        disk_spec.device.controllerKey = controller.key
        dev_changes.append(disk_spec)
        spec.deviceChange = dev_changes
        task = vm.ReconfigVM_Task(spec=spec)
        tasks.wait_for_tasks(si, [task])

def esxi_add_nic(host, usr, pwd, vm_name, network_name):
    try:
        si = connect.Connect(host=host, user=usr, pwd=pwd)
        vm_view = si.content.viewManager.CreateContainerView(si.content.rootFolder, [vim.VirtualMachine], True)
        uuid = ""
        for vm in vm_view.view:
            if vm.summary.config.name == vm_name:
                uuid = vm.summary.config.instanceUuid
                break
        if uuid == "":
            connect.Disconnect(si)
            return "Can't find VM(%s)!" % vm_name

        vm = si.content.searchIndex.FindByUuid(None, uuid, True, True)
        esxi_add_new_nic_process(vm, si, network_name)
        connect.Disconnect(si)
    except Exception, e:
        return "Create new drive on VM(%s) failed!" % vm_name

    return "Create new drive on VM(%s) successfully!" % vm_name

def get_obj(content, vimtype, name):
    obj = None
    container = content.viewManager.CreateContainerView(content.rootFolder,
                                                        vimtype, True)
    for view in container.view:
        if view.name == name:
            obj = view
            break
    return obj

def esxi_add_new_nic_process(vm, si, network_name):
    nic_prefix_label = 'Network adapter '
    nic_count = 0
    for dev in vm.config.hardware.device:
        if dev.deviceInfo.label.find(nic_prefix_label) >= 0:
            nic_count = nic_count + 1
    nic_label = nic_prefix_label + str(nic_count + 1)

    nic_spec = vim.vm.device.VirtualDeviceSpec()
    nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
    nic_spec.device = vim.vm.device.VirtualE1000()
    nic_spec.device.wakeOnLanEnabled = True
    nic_spec.device.addressType = 'generated'
    nic_spec.device.key = 4000
    nic_spec.device.deviceInfo = vim.Description()
    nic_spec.device.deviceInfo.label = nic_label

    nic_spec.device.backing = vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
    nic_spec.device.backing.network = get_obj(si.content, [vim.Network], network_name)
    nic_spec.device.backing.deviceName = network_name

    nic_spec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
    nic_spec.device.connectable.startConnected = True
    nic_spec.device.connectable.connected = True
    nic_spec.device.connectable.allowGuestControl = True

    dev_changes = []
    dev_changes.append(nic_spec)
    spec = vim.vm.ConfigSpec()
    spec.deviceChange = dev_changes
    task = vm.ReconfigVM_Task(spec=spec)
    tasks.wait_for_tasks(si, [task])

def esxi_trans_file(usr, host, pwd, filename, newfile):
    if newfile is not None:
        cmd = "scp %s %s@%s:%s" % (newfile, usr, host, filename)
        scp = pexpect.spawn(cmd)
    else:
        cmd = "scp %s@%s:%s ./" % (usr, host, filename)
        scp = pexpect.spawn(cmd)
    try:
        i = scp.expect(['[Pp]assword:',r'Are you sure you want to continue connecting \(yes/no\)\?',pexpect.EOF,pexpect.TIMEOUT])
        if i == 0:
            scp.sendline(pwd)
        elif i == 1:
            scp.sendline('yes\n')
            scp.expect('[Pp]assword:')
            scp.sendline(pwd)
    except pexpect.EOF:
        print "pexpect.EOF"
        scp.close()
        return -1
    except pexpect.TIMEOUT:
        print "pexpect.timeout"
        scp.close()
        return -2

    scp.expect(pexpect.EOF, timeout=300)
    scp.close()

def vpdu_ip_detect():
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind(('', 55555))
    while True:
        data, (host, port) = s.recvfrom(128)
        if host is not '':
            s.close()
            return host

def check_prompt_function(chan, output = False):
    resp = ""
    while resp.find("(vPDU)") < 0:
        resp = resp + chan.recv(64)
    if output is True:
        res_list = resp.split("\r\n")
        return ("\n").join(res_list[1:len(res_list)-1])
    return None

def vpdu_list_esxi_config_info(vpdu_ip):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(vpdu_ip, 20022)

    chan =ssh.invoke_shell()
    check_prompt_function(chan)
    chan.send("config esxi list\n")
    res = check_prompt_function(chan, output=True)

    ssh.close()
    return get_table_content(res)

def vpdu_set_pdu_info(vpdu_ip, name=None, database=None, snmpdata=None):
    if name is None and \
            database is None and \
            snmpdata is None:
        return None

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(vpdu_ip, 20022)

    chan = ssh.invoke_shell()
    check_prompt_function(chan)
    if name is not None:
        chan.send("config pdu set name {0}\n".format(name))
        check_prompt_function(chan)

    if database is not None:
        chan.send("config pdu set database {0}\n".format(database))
        check_prompt_function(chan)

    if snmpdata is not None:
        chan.send("config pdu set datadir {0}\n".format(snmpdata))
        check_prompt_function(chan)

    ssh.close()
    return "Success"

def vpdu_add_esxi_config_info(vpdu_ip, host, usr, pwd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(vpdu_ip, 20022)

    chan = ssh.invoke_shell()
    check_prompt_function(chan)
    chan.send("config esxi add %s %s %s\n" % (host, usr, pwd))
    check_prompt_function(chan)

    ssh.close()
    return "Success"

def vpdu_delete_esxi_config_info(vpdu_ip):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(vpdu_ip, 20022)

    chan =ssh.invoke_shell()
    check_prompt_function(chan)
    chan.send("config esxi delete \n")
    check_prompt_function(chan)

    ssh.close()
    return "Success"

def vpdu_map_add(vpdu_ip, vnode_dt, vnode_name, pdu, pdu_port):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(vpdu_ip, 20022)

    chan =ssh.invoke_shell()
    check_prompt_function(chan)
    chan.send("map add %s %s %s %s\n" % (vnode_dt, vnode_name, pdu, pdu_port))
    ssh.close()
    return "Success"

def vpdu_map_update(vpdu_ip, vnode_dt, vnode_name, pdu, pdu_port):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(vpdu_ip, 20022)

    chan =ssh.invoke_shell()
    check_prompt_function(chan)
    chan.send("map update %s %s %s %s\n" % (vnode_dt, vnode_name, pdu, pdu_port))
    ssh.close()
    return "Success"

def vpdu_pwd_add(vpdu_ip, pdu, pdu_port, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(vpdu_ip, 20022)

    chan =ssh.invoke_shell()
    check_prompt_function(chan)
    chan.send("password set %s %s %s\n" % (pdu, pdu_port, password))
    ssh.close()
    return "Success"

def vpdu_map_list(vpdu_ip):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(vpdu_ip, 20022)

    chan =ssh.invoke_shell()
    check_prompt_function(chan)
    chan.send("map list\n")
    res = check_prompt_function(chan, output=True)

    ssh.close()
    return get_table_content(res)

def vpdu_pwd_list(vpdu_ip, pdu_num):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(vpdu_ip, 20022)

    chan =ssh.invoke_shell()
    check_prompt_function(chan)
    chan.send("password list %s\n" % pdu_num)
    res = check_prompt_function(chan, output=True)

    ssh.close()
    return get_table_content(res)

def vpdu_map_delete(vpdu_ip, vnode_dt, vnode_name):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(vpdu_ip, 20022)

    chan =ssh.invoke_shell()
    check_prompt_function(chan)
    chan.send("map delete %s %s\n" % (vnode_dt, vnode_name))
    ssh.close()
    return "Success"

def vpdu_restart(vpdu_ip):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(vpdu_ip, 20022)

    chan =ssh.invoke_shell()
    check_prompt_function(chan)
    chan.send("vpdu restart\n")
    check_prompt_function(chan)

    ssh.close()
    return "Success"

def get_table_content(content):
    idx = 0
    line_list = []
    data = []

    if content.find("===") < 0:
        content = content.replace("\x1b[31m", "")
        content = content.replace("\x1b[0m", "")
        return json.dumps(content)

    for line in content.split("\n"):
        if idx % 2 == 1:
            line = line.replace("\x1b[92m", "")
            line = line.replace("\x1b[0m", "")
            line_list.append(line)
        idx = idx + 1

    for line in line_list[1:]:
        cs = line.split("|")
        keys = []
        for key in cs[1:len(cs) - 1]:
            keys.append(key.strip())
        data.append(keys)
    return json.dumps(data)

def singleDeploy(host, usr, pwd, dtst, powertype, duration, controlnetwork, nodetype, count, imagepath = IMAGE_PATH, img = None):
    """ Deploy single nodes to specific datastore of specific ESXi."""
    try:
        if img == None:
            image = findOva(nodetype.lower(), imagepath)
        else:
            image = "ova/" + img

        if 'on' == powertype:
            power = '--powerOn'
        else:
            power = ''

        count = int(count)
        duration = int(duration)
        for i in range(0, count):
            name = image.split('/')[-1] + '_' + str(time.time())
            deployVm(dtst, controlnetwork, name, image, usr, pwd, host, power)
            time.sleep(duration)

        return name
    except Exception, e:
        return e

def uploadOva(ova_file, filetype):
    ova_name = ova_file.name
    if filetype == "pdu":
        ova_name = "ova/pdu_" + ova_name
    else:
        ova_name = "ova/node_" + ova_name

    with open(ova_name, 'wb+') as destination:
        for chunk in ova_file.chunks():
            destination.write(chunk)
    return "Success"

def listOva(vmtype, imagepath=IMAGE_PATH):
    """ List a specific type of OVA files out."""
    files = []
    for path, dirnames, filenames in os.walk(imagepath):
        for filename in fnmatch.filter(filenames, ("*%s*" % (vmtype.lower()))):
            files.append(filename)

    return json.dumps(files)
