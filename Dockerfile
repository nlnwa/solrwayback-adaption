# This dockerfile sets up the SolrWayback bundle and attempts to run both Solr and Tomcat.
# To build the image, run:
# docker build . --tag solrwayback

# To run SolrWayback, you need to launch it with the following parameters
# docker run --publish 8080:8080 --publish 8983:8983  --volume <path/to/WARCs>:/warc-collection --tty --interactive solrwayback bash
# where <path/to/WARCs> is a file path that only contains WARC files and directories.

# When the container is running, run the following commands to start Solr and Tomcat:
# export SOLRWAYBACK_VERSION=4.4.2
# export APACHE_TOMCAT_VERSION=8.5.60
# export SOLR_VERSION=7.7.3
# ./unpacked-bundle/solrwayback_package_$SOLRWAYBACK_VERSION/solr-$SOLR_VERSION/bin/solr start
# ./unpacked-bundle/solrwayback_package_$SOLRWAYBACK_VERSION/apache-tomcat-$APACHE_TOMCAT_VERSION/bin/startup.sh

# You should now verify that the following links works with a browser:
# http://localhost:8080/solrwayback/
# http://localhost:8983/solr/#/

# If you have some WARC files you want to index, you can index them with the following commands:
# python3 index_it.py --collection <collection> --number-of-threads <threads> \
#     --warc-file-directory /warc-collection/<path/to/collection>
# <path/to/collection> must contain WARC files that all belong to the same collection
# Note: all of the WARC files in the directory will be indexed with the given collection
# Note: both neither solr or tomcat should be running when you call this command
# Note: index_it.py will stop both solr and tomcat on exit

FROM ubuntu:22.04

ENV SOLRWAYBACK_VERSION 4.4.2
ENV APACHE_TOMCAT_VERSION 8.5.60
ENV SOLR_VERSION 7.7.3

RUN apt-get update --assume-yes --quiet
RUN apt-get install wget unzip python3 --assume-yes --quiet

# Install dependencies
RUN apt-get install default-jre lsof curl --assume-yes --quiet

RUN useradd --create-home --shell /bin/bash builder
RUN chown builder:builder /home/builder -R

USER builder
WORKDIR /home/builder

# Download and unpack SolrWayback bundle
RUN mkdir --parents solrwayback-zip
RUN wget --quiet https://github.com/netarchivesuite/solrwayback/releases/download/${SOLRWAYBACK_VERSION}/solrwayback_package_${SOLRWAYBACK_VERSION}.zip \
    --output-document solrwayback-zip/bundle.zip

RUN mkdir unpacked-bundle
RUN unzip -q solrwayback-zip/bundle.zip -d unpacked-bundle
RUN rm --recursive solrwayback-zip

# Set up SolrWayback configuration
COPY --chown=builder solrwayback.properties .
COPY --chown=builder solrwaybackweb.properties .

# Verify that apache-tomcat and solr works, both need to be run together
RUN unpacked-bundle/solrwayback_package_${SOLRWAYBACK_VERSION}/apache-tomcat-${APACHE_TOMCAT_VERSION}/bin/startup.sh \
    && unpacked-bundle/solrwayback_package_${SOLRWAYBACK_VERSION}/solr-${SOLR_VERSION}/bin/solr start \
    && unpacked-bundle/solrwayback_package_${SOLRWAYBACK_VERSION}/solr-${SOLR_VERSION}/bin/solr stop -all \
    && unpacked-bundle/solrwayback_package_${SOLRWAYBACK_VERSION}/apache-tomcat-${APACHE_TOMCAT_VERSION}/bin/shutdown.sh

COPY --chown=builder nb_logo_desktop_red.svg .
COPY index_it.py .
