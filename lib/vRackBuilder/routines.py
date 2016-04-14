'''
*********************************************************
Copyright @ 2015 EMC Corporation All Rights Reserved
*********************************************************
'''

#! /usr/bin/python

import os
import sys
import subprocess
import ConfigParser
import fnmatch
import requests

import pexpect


def ssh_cmd(usr, host, pwd, cmd):
    """ ssh to a remote host and execute the command
    
    Args:
        usr (str):
            user name to log into the remote host
        host (str):
            ip address of the remote host
        pwd (str):
            password of the user to login 
        cmd (str):
            command need to be executed
            
    Returns:
        str: the output of the command successfully executed 
    """
    ssh = pexpect.spawn("ssh %s@%s '%s'" % (usr, host, cmd))
    try:
        i = ssh.expect(['[Pp]assword:',r'Are you sure you want to continue connecting \(yes/no\)\?',pexpect.EOF,pexpect.TIMEOUT])
        if i == 0:
            ssh.sendline(pwd)
        elif i == 1:
            ssh.sendline('yes\n')
            ssh.expect('[Pp]assword:')
            ssh.sendline(pwd)
    except pexpect.EOF:
        print "pexpect.EOF"
        ssh.close()
        return -1
    except pexpect.TIMEOUT:
        print "pexpect.timeout"
        ssh.close()
        return -2

    ssh.expect(pexpect.EOF, timeout=300)
    output = ssh.before
    ssh.close()
    return output

def trans_file(usr, host, pwd, filename):
    """ Transfer a file to remote host
    
    Args:
        usr (str):
            user name to log into the remote host
        host (str):
            ip address of the remote host
        pwd (str):
            password of the user to login 
        filename (str):
            the name of the file to transfer
    """
    scp = pexpect.spawn("scp %s %s@%s:/" % (filename, usr, host))
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
    output = scp.before
    print 'output', output
    scp.close()

def parseConfig(cfgfile='./conf/jMaster.conf', pycfgfile='./config.py'):
    """Parse the user configuration file and genearte the config.py file for project using.

    """
    if os.path.isfile(pycfgfile):
        os.remove(pycfgfile)

    fw = open(pycfgfile, 'a+')

    try:
        with open(cfgfile) as fp:
            for line in fp:
                try:
                    item = line.strip().split('=')
                    cfgline = item[0].upper() + ' = ' + item[1] + '\n'
                    fw.write(cfgline)
                except:
                    continue
    except:
        pass

    fw.close()    

def parseRules(rulesCfg='./conf/rules.conf', pyrules='./rules.py'):
    """Parse the rules.conf file and generate a rules.py file for projcet using.

    """
    if os.path.isfile(pyrules):
        os.remove(pyrules)

    fw = open(pyrules, 'a+')

    cp = ConfigParser.ConfigParser()
    cp.read(rulesCfg)

    for sec in cp.sections():
        dictline = '%s = {\n' % sec
        fw.write(dictline)
        for opt in cp.options(sec):
            itemline = '\t\'%s\' : %s,\n' % (opt, cp.get(sec,opt))
            fw.write(itemline)
        fw.write('\t}\n')
    fw.close()

def ShellCmd(cmd):
    """ Execute one shell command."""

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output = p.stdout.read()
    return output.strip('\n')

def findOva(vmtype, image_path):
    """ Find the full name of image through vm type.

        Note:
            if there are multiple images with same type but different version number,
            should return the newest one(version number is the biggest one in name."
    """
    files = []
    for path, dirnames, filenames in os.walk(image_path):
        for filename in fnmatch.filter(filenames, ("*%s*" % (vmtype))):
            files.append(os.path.join(path, filename))
    
    if len(files):
        return max(files, key=lambda x: int(x.split('.')[0].split('_')[-1]))
    else:
        print 'Didn\'t find an image match with %s.' % vmtype

def deployVm(datastore, controlnetwork, name, image, usr, pwd, host, power='', diskmd='thin'):
    """ Deploy the VM to specific ESXi  """

    ovftool = ShellCmd("which ovftool")

    if controlnetwork=="0":
        cmd = 'echo "yes" | %s --diskMode=%s --datastore="%s" --name=%s %s %s vi://%s:%s@%s' % \
              (ovftool, diskmd, datastore, name, power, image, usr, pwd, host)
    else:
       cmd = 'echo "yes" | %s --diskMode=%s --datastore="%s" --network="%s" --name=%s %s %s vi://%s:%s@%s' % \
             (ovftool, diskmd, datastore, controlnetwork, name, power, image, usr, pwd, host)

    print cmd

    output = ShellCmd(cmd)
    print output


def downloadFile(url, imagepath):
    """ Download a specific type and version OVA from build farm."""
    
    filename = url.split('/')[-1]
    fullname = imagepath + filename
    
    if os.path.isfile(fullname):
        return fullname

    try:
        req = requests.get(url, stream=True)
        req.raise_for_status()
        with open(fullname, 'wb') as f:
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        return fullname
    except Exception,e:
        return e


