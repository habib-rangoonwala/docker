###################################
# Author: Habib Rangoonwala
# Created: 21-Jan-2016
# Updated: 29-Jan-2016
###################################

import os
import random
import string
import socket

# Functions
def randomName():
  return ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(6)])

def editMode():
  edit()
  startEdit(3000000,300000,'true')

def editActivate():
  save()
  activate(block="true")

# AdminServer details
username  = os.environ.get('ADMIN_USERNAME', 'weblogic')
password  = os.environ.get('ADMIN_PASSWORD')
adminhost = os.environ.get('ADMIN_HOST', 'wlsadmin')
adminport = os.environ.get('ADMIN_PORT', '8001')
cluster_name = os.environ.get("CLUSTER_NAME", "DEFAULT_CLUSTER")

# NodeManager details
nmname = os.environ.get('NM_NAME',socket.gethostname())

# ManagedServer details
msinternal = socket.gethostbyname(socket.gethostname())
msname = os.environ.get('MS_NAME', 'MS_' + socket.gethostname())
mshost = os.environ.get('MS_HOST', socket.gethostbyname(socket.gethostname()))
msport = os.environ.get('MS_PORT', '7001')
memargs = os.environ.get('USER_MEM_ARGS', '')

# Connect to the AdminServer
# ==========================
connect(username, password, 't3://' + adminhost + ':' + adminport)

# Create a ManagedServer
# ======================
editMode()
cd('/')
cmo.createServer(msname)

cd('/Servers/' + msname)
cmo.setMachine(getMBean('/Machines/' + nmname))
cmo.setCluster(getMBean('/Clusters/' + cluster_name))

# Default Channel for ManagedServer
# ---------------------------------
cmo.setListenAddress(msinternal)
cmo.setListenPort(int(msport))
cmo.setListenPortEnabled(true)
cmo.setExternalDNSName(mshost)

# Disable SSL for this ManagedServer
# ----------------------------------
cd('/Servers/' + msname + '/SSL/' + msname)
cmo.setEnabled(false)


# Custom Startup Parameters because NodeManager writes wrong AdminURL in startup.properties
# -----------------------------------------------------------------------------------------
cd('/Servers/' + msname + '/ServerStart/' + msname)
arguments = '-Djava.security.egd=file:/dev/./urandom -Dweblogic.Name=' + msname + ' -Dweblogic.management.server=http://' + adminhost + ':' + adminport + ' ' + memargs
cmo.setArguments(arguments)
editActivate()

# Start Managed Server
# ------------
try:
    start(msname, 'Server')
except:
    dumpStack()

# Exit
# =========
exit()
