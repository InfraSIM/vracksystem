'''
*********************************************************
Copyright @ 2015 EMC Corporation All Rights Reserved
*********************************************************
'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import getopt, sys, json
from terminaltables import AsciiTable

class ESXIClient:
    def __init__(self, keys):
        self.api_host_keys = keys

    def list_esxi_nodes(self):
        r = requests.get("http://" + self.api_host_keys["host"] + "/api/v1/esxi/", auth=(self.api_host_keys["user"], self.api_host_keys["password"]))
        table_data = [["ID", "User Name", "Password", "ESXi IP"]]
        for res in r.json():
            table_data.append([str(res['id']), res['username'], res['password'], res['esxiIP']])
        table = AsciiTable(table_data)
        print table.table

    def add_esxi_node(self):
        esxiIP = raw_input("ESXi IP: ")
        username = raw_input("User Name: ")
        password = raw_input("Password: ")
        r = requests.post("http://" + self.api_host_keys["host"] + "/api/v1/esxi/", auth=(self.api_host_keys["user"], self.api_host_keys["password"]),
                            data = {"esxiIP":esxiIP, "username":username, "password":password} )
        if "id" in r.json().keys():
            print "New Node %s is Added" % r.json()["id"]
        else:
            print "Error: %s" % r.text

    def del_esxi_node(self):
        node_id = raw_input("The node you want to DELETE: ")
        yes = raw_input("\nConfirmed? (yes/no)")
        if yes == "yes" or yes == 'y' or yes == '':
            requests.delete("http://" + self.api_host_keys["host"] + "/api/v1/esxi/" + node_id + "/", auth=(self.api_host_keys["user"], self.api_host_keys["password"]))
            print "Node %s deleted successfully" % node_id

    def show_esxi_node(self):
        node_id = raw_input("The ESXi node you want to show: ")
        table_data = [["ID", "User Name", "Password", "ESXi IP"]]
        r = requests.get("http://" + self.api_host_keys["host"] + "/api/v1/esxi/" + node_id + "/", auth=(self.api_host_keys["user"], self.api_host_keys["password"]))
        if r.status_code == 404:
            print "This ESXi is not existing!"
            return;

        res = r.json()
        table_data.append([str(res['id']), res['username'], res['password'], res['esxiIP']])
        table = AsciiTable(table_data)
        print table.table

        try:
            r = requests.get("http://" + self.api_host_keys["host"] + "/api/v1/esxi/" + node_id + "/hardware", auth=(self.api_host_keys["user"], self.api_host_keys["password"]))
            print "Hardware Info: " + r.json()
            r = requests.get("http://" + self.api_host_keys["host"] + "/api/v1/esxi/" + node_id + "/networks", auth=(self.api_host_keys["user"], self.api_host_keys["password"]), timeout=10)
            print "Networks: "  + r.json()
            r = requests.get("http://" + self.api_host_keys["host"] + "/api/v1/esxi/" + node_id + "/datastores", auth=(self.api_host_keys["user"], self.api_host_keys["password"]), timeout=10)
            print "DataStores: " + r.json()
        except requests.exceptions.Timeout:
            print "Fetch Node(%s) Network and DataStore Time out" % node_id

    def esxi_list_all_vms(self):
        node_id = raw_input("The ESXi you want to use: ")
        r = requests.get("http://" + self.api_host_keys["host"] + "/api/v1/esxi/" + node_id + "/getvms", auth=(self.api_host_keys["user"], self.api_host_keys["password"]))
        if r.status_code == 404:
            print "The ESXi not is not existed!"
            return

        vms = json.loads(r.json())
        table_data = [["VM Name", "UUID", "VM DataStore", "Power Status", "IP Address"]]
        for vm in vms:
            table_data.append([vm["name"], vm["uuid"], vm["datastore"], vm["status"], json.dumps(vm["ip"])])
        table = AsciiTable(table_data)
        print table.table

    def esxi_poweron_vm(self):
        node_id = raw_input("The ESXi you want to use: ")
        name = raw_input("The VM name: ")
        r = requests.post("http://" + self.api_host_keys["host"] + "/api/v1/esxi/" + node_id + "/poweronvm", auth=(self.api_host_keys["user"], self.api_host_keys["password"]),
            data = {"name":name} )
        if r.status_code == 200:
            print r.text
        else:
            print "The ESXi is not existed!"

    def esxi_poweroff_vm(self):
        node_id = raw_input("The ESXi you want to use: ")
        name = raw_input("The VM name: ")
        r = requests.post("http://" + self.api_host_keys["host"] + "/api/v1/esxi/" + node_id + "/poweroffvm", auth=(self.api_host_keys["user"], self.api_host_keys["password"]),
            data = {"name":name} )
        if r.status_code == 200:
            print r.text
        else:
            print "The ESXi is not existed!"

    def esxi_reset_vm(self):
        node_id = raw_input("The ESXi you want to use: ")
        name = raw_input("The VM name: ")
        r = requests.post("http://" + self.api_host_keys["host"] + "/api/v1/esxi/" + node_id + "/resetvm", auth=(self.api_host_keys["user"], self.api_host_keys["password"]),
            data = {"name":name} )
        if r.status_code == 200:
            print r.text
        else:
            print "The ESXi is not existed!"

    def esxi_destroy_vm(self):
        node_id = raw_input("The ESXi you want to use: ")
        name = raw_input("The VM name: ")
        r = requests.post("http://" + self.api_host_keys["host"] + "/api/v1/esxi/" + node_id + "/destroyvm", auth=(self.api_host_keys["user"], self.api_host_keys["password"]),
            data = {"name":name} )
        if r.status_code == 200:
            print r.text
        else:
            print "The ESXi is not existed!"

    def esxi_add_drive(self):
        node_id = raw_input("The ESXi you want to use: ")
        name = raw_input("VM name: ")
        size = raw_input("Disk Size(G): ")
        r = requests.post("http://" + self.api_host_keys["host"] + "/api/v1/esxi/" + node_id + "/adddrive", auth=(self.api_host_keys["user"], self.api_host_keys["password"]),
            data = {"size":size, "name":name} )
        if r.status_code == 200:
            print r.text
        else:
            print "ESXi Create New Drive Failed"

    def esxi_add_nic(self):
        node_id = raw_input("The ESXi you want to use: ")
        name = raw_input("VM Name: ")
        network = raw_input("Network Name: ")

        r = requests.post("http://" + self.api_host_keys["host"] + "/api/v1/esxi/" + node_id + "/addnic", auth=(self.api_host_keys["user"], self.api_host_keys["password"]),
                        data = {"name":name, "network":network} )
        if r.status_code == 200:
            print r.text
        else:
            print "ESXi Attach New Nic Failed"

    def deploy_esxi_node(self):
        node_id = raw_input("The ESXi you want to deploy node: ")
        dt = raw_input("Please input the datastore: ")
        nodetype = raw_input("Please input the nodetype: ")

        r = requests.post("http://" + self.api_host_keys["host"] + "/api/v1/esxi/" + node_id + "/deploy", auth=(self.api_host_keys["user"], self.api_host_keys["password"]),
                        data = {"datastore":dt, "power":"on", "nodetype":nodetype} )
        if r.status_code == 200:
            if type == 'vpdu':
                print r.text
            else:
                print "New vNode(%s) deployed successfully" % (r.text)
        else:
            print "Deploy %s on ESXi(%s) failed" % (type, node_id)

    def list_vpdu_esxi_config_info(self):
        node_id = raw_input("The ESXi you want to show vPDU info: ")
        vpdu_ip = raw_input("The vPDU ip address: ")
        r = requests.post("http://" + self.api_host_keys["host"] + "/api/v1/esxi/" + node_id + "/vpduhostlist", auth=(self.api_host_keys["user"], self.api_host_keys["password"]),
                          data = {"ip":vpdu_ip})
        if r.status_code == 200:
            try:
                table_data = [["ESXi ID", "ESXi Host", "USR", "PASSWORD"]]
                for res in json.loads(r.json()):
                    table_data.append(res)
                table = AsciiTable(table_data)
                print table.table
            except Exception, e:
                print r.json()
        else:
            print "Get vPDU Host configuration info failed!"

    def add_vpdu_esxi_config_info(self):
        node_id = raw_input("The ESXi you want to show vPDU info: ")
        vpdu_ip = raw_input("The vPDU ip address: ")
        r = requests.post("http://" + self.api_host_keys["host"] + "/api/v1/esxi/" + node_id + "/vpduhostadd", auth=(self.api_host_keys["user"], self.api_host_keys["password"]),
                          data = {"ip":vpdu_ip})
        if r.status_code == 200:
             print "Add vPDU Host configuration info %s" % r.text
        else:
            print "Add vPDU Host configuration info failed!"

    def delete_vpdu_esxi_config_info(self):
        node_id = raw_input("The ESXi you want to delete vPDU info: ")
        vpdu_ip = raw_input("The vPDU ip address: ")
        r = requests.post("http://" + self.api_host_keys["host"] + "/api/v1/esxi/" + node_id + "/vpduhostdel", auth=(self.api_host_keys["user"], self.api_host_keys["password"]),
                          data = {"ip":vpdu_ip})
        if r.status_code == 200:
             print "Delete vPDU ESXi info %s" % r.text
        else:
            print "Delete vPDU Host configuration info failed!"

    def add_vpdu_map(self):
        node_id = raw_input("The ESXi you want to deploy node: ")
        vpdu_ip = raw_input("The vPDU ip address: ")
        dt = raw_input("Please input the datastore: ")
        name = raw_input("Please input the vmname: ")
        pdu = raw_input("Please input the pdu number(1-6): ")
        port = raw_input("Please input the pdu port number(1-24): ")
        r = requests.post("http://" + self.api_host_keys["host"] + "/api/v1/esxi/" + node_id + "/vpdumapadd", auth=(self.api_host_keys["user"], self.api_host_keys["password"]),
                        data = {"dt":dt, "name":name, "ip":vpdu_ip, "pdu":pdu, "port":port} )
        if r.status_code == 200:
            print "Add to vPDU map %s" % (r.text)
        else:
            print "Add to vPDU map failed"

    def list_vpdu_map(self):
        node_id = raw_input("The ESXi you want to show vPDU Map info: ")
        vpdu_ip = raw_input("The vPDU ip address: ")
        r = requests.post("http://" + self.api_host_keys["host"] + "/api/v1/esxi/" + node_id + "/vpdumaplist", auth=(self.api_host_keys["user"], self.api_host_keys["password"]),
                          data = {"ip":vpdu_ip})
        if r.status_code == 200:
            table_data = [["PDU", "PORT", "DataStore", "VM Name"]]
            for res in json.loads(r.json()):
                table_data.append(res)
            table = AsciiTable(table_data)
            print table.table
        else:
            print "Get vPDU Map info failed"

    def esxi_list_ova(self):
        type_list = ["node", "pdu"]

        for t in type_list:
            r = requests.post("http://" + self.api_host_keys["host"] + "/api/v1/ova/list", auth=(self.api_host_keys["user"], self.api_host_keys["password"]), data = {"type":t})
            print "%s images ==> %s" % (t, r.json())

    def upload_ova(self):
        type = raw_input("OVA Type: ")
        name = raw_input("OVA Name: ")
        if type == "pdu":
            files = {"file":(name, open(name, 'rb'), 'application/vpdu')}
        else:
            files = {"file":(name, open(name, 'rb'), 'application/vnode')}
        r = requests.post("http://" + self.api_host_keys["host"] + "/api/v1/ova/upload", auth=(self.api_host_keys["user"], self.api_host_keys["password"]), files=files)
        print r.json()

    def parse_input(self, cmd):
        if cmd == "listesxi":
            self.list_esxi_nodes()
        elif cmd == "addesxi":
            self.add_esxi_node()
        elif cmd == "delesxi":
            self.del_esxi_node()
        elif cmd == "showesxi":
            self.show_esxi_node()
        elif cmd == "deployesxi":
            self.deploy_esxi_node()
        elif cmd == "listvm":
            self.esxi_list_all_vms()
        elif cmd == "poweronvm":
            self.esxi_poweron_vm()
        elif cmd == "poweroffvm":
            self.esxi_poweroff_vm()
        elif cmd == "resetvm":
            self.esxi_reset_vm()
        elif cmd == "destroyvm":
            self.esxi_destroy_vm()
        elif cmd == "adddrive":
            self.esxi_add_drive()
        elif cmd == "addnic":
            self.esxi_add_nic()
        elif cmd == "deploy":
            self.deploy_esxi_node()
        elif cmd == "listvpduhostinfo":
            self.list_vpdu_esxi_config_info()
        elif cmd == "addvpduhostinfo":
            self.add_vpdu_esxi_config_info()
        elif cmd == "delvpduhostinfo":
            self.delete_vpdu_esxi_config_info()
        elif cmd == "addvpdumap":
            self.add_vpdu_map()
        elif cmd == "listvpdumap":
            self.list_vpdu_map()
        elif cmd == "listova":
            self.esxi_list_ova()
        elif cmd == "uploadova":
            self.upload_ova()
        elif cmd == "version":
            print ("vRack CLI version: 1.3")
        elif cmd == "help":
            print("\tESXI Manage:")
            print("\tlistesxi:\tList existing ESXi machines")
            print("\tshowesxi:\tShow existing ESXi machines node")
            print("\taddesxi:\tAdd existing ESXi machines")
            print("\tdelesxi:\tDelete existing ESXi machines\n")
            print("\tESXI VM Manage:")
            print("\tlistvm:\t\tList All VirtualMachine Details")
            print("\tpoweronvm:\tPower on the specified VM")
            print("\tpoweroffvm:\tPower off the specified VM")
            print("\tresetvm:\tReset VM")
            print("\tdestroyvm:\tDestroy VM")
            print("\tadddrive:\tCreate new drive for specified VM")
            print("\taddnic:\t\tAttach the new nic")
            print("\tdeploy:\t\tDeploy a new VM\n")
            print("\tvPDU Manage: ")
            print("\tlistvpduhostinfo:\tlist vpdu-esxi configuration info")
            print("\taddvpduhostinfo:\tAdd vpdu-esxi configuration info")
            print("\tdelvpduhostinfo:\tRemove vpdu-esxi configuration info")
            print("\taddvpdumap:\tAdd a new vPDU mapping")
            print("\tlistvpdumap:\tList the existing vPDU mapping\n")
            print("\tImages Manage: ")
            print("\tlistova:\tList existing OVA images: node, pdu")
            print("\tuploadova:\tUpload existing OVA images")
            print("\n\thelp:\t\tPrint this manual")
            print("\tversion:\tCLI version")
        else:
            print "Unsupport Command"

    def esxi_run(self):
        try:
            requests.get("http://" + self.api_host_keys["host"] + "/api/v1/esxi/", auth=(self.api_host_keys["user"], self.api_host_keys["password"]))
        except requests.exceptions.ConnectionError:
            print "Can't connect to Web server, please check your usr/password/ip address"
            sys.exit(-1)

        while True:
            input = raw_input("ESXi> ")
            if input == "q" or input == "quit":
                print "See you next time.\n"
                break
            self.parse_input(input.strip())
            print("")
