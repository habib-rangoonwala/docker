#!/bin/bash

#############################################
# Author: Habib Rangoonwala
# Created: 09-Jan-2016
# Updated: 28-Jan-2016
# Howto: 
# This script is set as CMD in Dockerfile
#############################################

# USE the trap if you need to also do manual cleanup after the service is stopped,
#     or need to start multiple services in the one container
trap "echo 'replace this with script to execute'" HUP INT QUIT KILL TERM

# start service in background here
echo "Adding this service to ETCD"

# find the docker_host_ip
DOCKER_HOST_IP=`/sbin/ip route|awk '/default/ { print $3 }'`
#curl -L -X PUT http://${DOCKER_HOST_IP}:2379/v2/keys/it/platform/apache -d value="$HOSTNAME"

# LD_LIBRARY_PATH  is required for mod_wl to work
# if not set you get this error
# Cannot load modules/mod_wl_24.so into server: libopmnsecure.so: cannot open shared object file: No such file or directory
export LD_LIBRARY_PATH=/usr/local/apache2/modules

echo "Starting Apache"
/usr/local/apache2/bin/apachectl start -D FOREGROUND

echo "[hit enter key to exit] or run 'docker stop <container>'"
read myval

# stop service and clean up here
echo "Stopping Apache"
/usr/local/apache2/bin/apachectl stop

echo "Removing this service from ETCD"
#curl -L -X DELETE http://${DOCKER_HOST_IP}:2379/v2/keys/it/platform/apache

echo "exited $0"
