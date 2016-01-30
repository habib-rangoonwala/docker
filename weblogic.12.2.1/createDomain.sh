#!/bin/bash

########################################################################################
# Author: Habib Rangoonwala
# Created: 21-Jan-2016
# Updated: 29-Jan-2016
# Usage:
#  createDomain.sh <instancename>
#    <instancename> is used to as prefix/suffix for naming different components
########################################################################################


# to debug python, add -Dpython.verbose=debug
CONFIG_JVM_ARGS="${CONFIG_JVM_ARGS} -Dweblogic.security.SSL.ignoreHostnameVerification=true"

instancename=`echo $1|awk '{ print toupper($1) }'`
export NEW_DOMAIN_NAME="${instancename}_DOMAIN"
export CLUSTER_NAME="${instancename}_CLUSTER"
export ADMIN_HOST="wlsadmin$instancename"

#create the domain
${PAAS_HOME}/wlserver/common/bin/wlst.sh -skipWLSModuleScanning ${PAAS_HOME}/create-wls-domain.py

export DOMAIN_NAME=$NEW_DOMAIN_NAME

# unset $1 so that setDomainEnv.sh does not get any parameters
# due to some bug, if shift is not used setDomainEnv.sh will use $1 to launch managed server and fail
shift
. ${PAAS_HOME}/user_projects/domains/${DOMAIN_NAME}/bin/setDomainEnv.sh

#create boot.properties
mkdir -p ${PAAS_HOME}/user_projects/domains/${DOMAIN_NAME}/servers/AdminServer/security
echo "username=weblogic" > ${PAAS_HOME}/user_projects/domains/${DOMAIN_NAME}/servers/AdminServer/security/boot.properties 
echo "password=$ADMIN_PASSWORD" >> ${PAAS_HOME}/user_projects/domains/${DOMAIN_NAME}/servers/AdminServer/security/boot.properties 

#check how to persistently store this information
echo ". ${PAAS_HOME}/user_projects/domains/${DOMAIN_NAME}/bin/setDomainEnv.sh" >> ${PAAS_HOME}/.bashrc && \
echo "export PATH=$PATH:${PAAS_HOME}/wlserver/common/bin:${PAAS_HOME}/user_projects/domains/${DOMAIN_NAME}/bin" >> ${PAAS_HOME}/.bashrc

# pack the domain and change the permission so that other managed server process can read this domain template file
pack.sh -domain $DOMAIN_HOME -template $DOMAIN_HOME/${instancename}_DOMAIN.jar -template_name ${instancename}_DOMAIN -managed=true
chmod 775  $DOMAIN_HOME/${instancename}_DOMAIN.jar

startWebLogic.sh
