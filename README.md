Welcome to vRackSystem!
===================

vRackSystem is a tool to easily build a virtual Rack. Please follow below document to setup the vracksystem server.

----------


What vRackSystem can do currently?
-------------
- Deploy the virtual nodes(vNode and vPDU) built by **InfraSIM**.
- Manage ESXi resources.
- Mapping vPDU and vNode.
- More features are comming...

> **Note:**
> 
> - [InfraSIM](https://github.com/InfraSIM) is an open source project and it simulates the interfaces/behaviors of hardware devices a virtual environment. More information can be got from [InfraSIM Document](http://infrasim.readthedocs.org/en/latest/).

vRackSystem Server Setup
-------------
- vRackSystem server must be an Linux Server with **ssh installed and ssh public key generated**.
- vRackSystem server must have connection with all the ESXi host that need to be managed.
- vRackSystem server should have an external network. So it can be accessed by external PC.
- **RackHD** can also be setup in the environment to control vNode and vPDU.

> **Note:**
> 
> - [RackHD](https://github.com/RackHD) is an open source project that provides hardware orchestration and management through APIs. More information can be got from [RackHD Document](http://rackhd.readthedocs.org/en/latest/).


![vRackSystem Network setup with RackHD ](/app/static/app/img/networkwithrackhd.png)

![vRackSystem Network setup without RackHD ](/app/static/app/img/networkwithoutrackhd.png)

vRackSystem Environment Setup Steps
-------------
#### Install python(2.x version except 2.7.9)
```
sudo apt-get install python
sudo apt-get install python-pip
sudo apt-get install python-dev
sudo apt-get install python-setuptools
```
Check whether python was successfully installed and the version is correct.
```
python --version
```
#### Install VMWare ovftool

- Download [VMWare OVF bundle](https://my.vmware.com/group/vmware/details?productId=491&downloadGroup=OVFTOOL410) (4.1.0 version, for Linux). Then put the bundle file to the vracksystem server.
- Install the OVF tool
```
sudo bash VMware-ovftool-4.1.0-2459827-lin.x86_64.bundle
```
#### Install mysql
```
sudo apt-get install mysql-server
sudo apt-get install python-mysqldb
```
#### Import database
- Get the exiting databases file(vracksystem.sql) from vRackSystem project directory.
- Enter mysql by below command.

```
mysql -u <your mysql account> -p
```
- Input your mysql password.
- Import the databases files.
```
source /path/to/vracksystem.sql
```
#### Clone vracksystem code from github
#### Change **vracksystem/ova/** folder privilege to 755.
```
cd vracksystem
sudo chmod -R 755 ova/
```
#### Install python packages.
```
cd vracksystem
sudo pip install -r requirements.txt
```
#### Update the db connection information. 
Change the username and password to align with your own account information in the /vracksystem/AutodeployUI/settings.py.
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'AutoDeployUI',
        'USER': '<your mysql account>',
        'PASSWORD': '<your mysql password>',
        'HOST':'localhost',
    }
}
```
#### Prepare OVA images
Put your OVA images(vNode and vPDU images) to /vracksystem/ova/.
#### Start vRackProject
```
cd vracksystem
python manage.py runserver 0.0.0.0:<port>
```
#### Access vRackSystem GUI
   Access vRackSystem by http://&lt;vracksystem server IP&gt;:&lt;port&gt;/ on your external PC.