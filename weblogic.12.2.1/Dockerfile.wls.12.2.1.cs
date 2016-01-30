############################################################################
# Author: Habib Rangoonwala
# Created: 09-Jan-2016
# Updated: 28-Jan-2016
# USAGE: 
# Run:
#   $ docker build -t habib-rangoonwala/weblogic:12.2.1-cs -f Dockerfile.wls.12.2.1.cs .
############################################

FROM habib-rangoonwala/weblogic:12.2.1-infra

# Maintainer
# ----------
MAINTAINER Habib Rangoonwala

# Copy customization scripts to the image
# ----------------------------------------
COPY * ${PAAS_HOME}/

CMD ["startWebLogic.sh"]
