##############################################
# Author: Habib Rangoonwala
# Created: 09-Jan-2016
# Updated: 28-Jan-2016
# USAGE: 
# $ docker build -t habib-rangoonwala/apachewls:2.4.18-infra -f Dockerfile.httpd.2.4.18.infra .
##############################################

FROM httpd
MAINTAINER Habib Rangoonwala
#ENTRYPOINT ["/usr/local/apache2/bin/container-apachectl.sh"]

# Copy mod_wl files to apache/modules
COPY *.so /usr/local/apache2/modules/

RUN apt-get update && apt-get install -y \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

#CMD ["bash"]
#CMD ["-d FOREGROUND"]
