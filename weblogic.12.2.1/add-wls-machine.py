###################################
# Author: Habib Rangoonwala
# Created: 21-Jan-2016
# Updated: 28-Jan-2016
###################################

import os
import socket

# Functions
def editMode():
  edit()
  startEdit(3000000,300000,'true')

def editActivate():
  save()
  activate(block="true")

# Variables
# =========

# AdminServer details
username  = os.environ.get('ADMIN_USERNAME', 'weblogic')
password  = os.environ.get('ADMIN_PASSWORD')
adminhost = os.environ.get('ADMIN_HOST', 'wlsadmin')
adminport = os.environ.get('ADMIN_PORT', '8001')
domainhome = os.environ.get('DOMAIN_HOME', '')
domainname = os.environ.get('DOMAIN_NAME', 'DEFAULT_DOMAIN')

# NodeManager details
nmname = os.environ.get('NM_NAME', socket.gethostname())
nmhost = os.environ.get('NM_HOST', socket.gethostbyname(socket.gethostname()))
nmport = os.environ.get('NM_PORT', '5556')

#start Admin Server
#nmStart('AdminServer')
#nmServerStatus('AdminServer')

#startServer('AdminServer',domainname,'t3://' + adminhost + ':' + adminport,username,password,domainhome,'true',60000,'false')


# Connect to the AdminServer
# ==========================
connect(username, password, 't3://' + adminhost + ':' + adminport)

# Create a Machine
# ================
editMode()
cd('/')
cmo.createMachine(nmname)
cd('/Machines/' + nmname +'/NodeManager/' + nmname)
cmo.setListenPort(int(nmport))
cmo.setListenAddress(nmhost)
cmo.setNMType('Plain')
editActivate()

# Exit
# ====
exit()
