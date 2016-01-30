############################################
# Author: Habib Rangoonwala
# Created: 09-Jan-2016
# Updated: 29-Jan-2016
# USAGE: 
# $ docker build -t habib-rangoonwala/apachewls:2.4.18-cs -f Dockerfile.httpd.2.4.18.cs .
############################################

FROM habib-rangoonwala/apachewls:2.4.18-infra
MAINTAINER Habib Rangoonwala
#ENTRYPOINT ["/usr/local/apache2/bin/container-apachectl.sh"]

COPY container-apachectl.sh /usr/local/apache2/bin/

#CMD ["bash"]
#CMD ["-d FOREGROUND"]
