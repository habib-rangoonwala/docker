#!/bin/bash

########################################################################################
# Author: Habib Rangoonwala
# Created: 21-Jan-2016
# Updated: 29-Jan-2016
# Usage:
#  createServer.sh <instancename>
#    <instancename> is used to as prefix/suffix for naming different components
########################################################################################


instancename="$1"
export DOMAIN_HOME="$PAAS_HOME/user_projects/domains/${instancename}_DOMAIN"

# start by unpacking the domain template created in createDomain.sh script
${PAAS_HOME}/wlserver/common/bin/unpack.sh -overwrite_domain true -domain $DOMAIN_HOME -template $DOMAIN_HOME/${instancename}_DOMAIN.jar

# now we have unpacked the domain so we can source domain environment file
. ${PAAS_HOME}/wls.env

export ADMIN_HOST="wlsadmin$instancename"
export CLUSTER_NAME="${instancename}_CLUSTER"

CONFIG_JVM_ARGS="${CONFIG_JVM_ARGS} -Dweblogic.security.SSL.ignoreHostnameVerification=true"
WLST="wlst.sh -skipWLSModuleScanning"

# Start Node Manager
nohup startNodeManager.sh > log.nm &
sleep 5

# Add a Machine to the AdminServer
$WLST ${PAAS_HOME}/add-wls-machine.py > `hostname`.log

# Wait and add a new Managed Server
$WLST ${PAAS_HOME}/add-managed-server.py >> `hostname`.log

# print log
tail -f `hostname`.log
