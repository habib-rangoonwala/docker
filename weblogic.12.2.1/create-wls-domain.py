###############################
# Author: Habib Rangoonwala
# Created: 21-Jan-2016
# Updated: 29-Jan-2016
###############################
domain_name  = "base_domain"
admin_port   = int(os.environ.get("ADMIN_PORT", "8001"))
admin_pass   = os.environ.get("ADMIN_PASSWORD", "welcome1")
cluster_name = os.environ.get("CLUSTER_NAME", "Cluster-Docker")
paas_home = os.environ.get("PAAS_HOME", "/paas")
domain_path  = paas_home + '/user_projects/domains/' + domain_name

# Open default domain template
# ======================
readTemplate(paas_home + "/wlserver/common/templates/wls/wls.jar")

# Configure the Administration Server and SSL port.
# =========================================================
cd('/Servers/AdminServer')
set('ListenAddress', '')
set('ListenPort', admin_port)

# Define the user password for weblogic
# =====================================
cd('/Security/' + domain_name + '/User/weblogic')
cmo.setPassword(admin_pass)

# Create a JMS Server
# ===================
cd('/')
create('myJMSServer', 'JMSServer')

# Create a JMS System resource
# ============================
cd('/')
create('myJmsSystemResource', 'JMSSystemResource')
cd('JMSSystemResource/myJmsSystemResource/JmsResource/NO_NAME_0')

# Create a JMS Queue and its subdeployment
# ========================================
myq = create('myQueue','Queue')
myq.setJNDIName('jms/myqueue')
myq.setSubDeploymentName('myQueueSubDeployment')

cd('/JMSSystemResource/myJmsSystemResource')
create('myQueueSubDeployment', 'SubDeployment')

# Target resources to the servers
# ===============================
cd('/')
assign('JMSServer', 'myJMSServer', 'Target', 'AdminServer')
assign('JMSSystemResource.SubDeployment', 'myJmsSystemResource.myQueueSubDeployment', 'Target', 'myJMSServer')

# Write the domain and close the domain template
# ==============================================
setOption('OverwriteDomain', 'true')
setOption('ServerStartMode','prod')

cd('/NMProperties')
set('ListenAddress','')
set('ListenPort',5556)
set('NativeVersionEnabled', 'false')
set('StartScriptEnabled', 'false')
set('SecureListener', 'false')

# Set the Node Manager user name and password
cd('/SecurityConfiguration/' + domain_name)
set('NodeManagerUsername', 'weblogic')
set('NodeManagerPasswordEncrypted', admin_pass)

# Define a WebLogic Cluster
# =========================
cd('/')
create(cluster_name, 'Cluster')

cd('/Clusters/' + cluster_name)
cmo.setClusterMessagingMode('unicast')

# Write Domain
# ============
setOption('OverwriteDomain', 'true')
domain_name  = os.environ.get("NEW_DOMAIN_NAME", "base_domain")
domain_path  = paas_home + '/user_projects/domains/' + domain_name
writeDomain(domain_path)
closeTemplate()

# Exit WLST
# =========
exit()
