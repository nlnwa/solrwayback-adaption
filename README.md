# SolrWayback container images

This repository builds and publishes container images from [SolrWayback releases](https://github.com/netarchivesuite/solrwayback/releases).

## Images

### Solrwayback

```shell
docker run -p 8080:8080 ghcr.io/nlnwa/solrwayback
```

This will start SolrWayback which can be accessed at <http://localhost:8080/solrwayback>, but since the image is configured to access the Solr collection at `http://localhost:8983/solr/netarchivebuilder` it will give you an error message when run in isolation.

### Warc indexer

```shell
$ docker run ghcr.io/nlnwa/warc-indexer -h

warc-indexer.sh

Parallel processing of WARC files using webarchive-discovery from UKWA:
https://github.com/ukwa/webarchive-discovery

The scripts keeps track of already processed WARCs by keeping the output
logs from processing of each WARC. These are stored in the folder
/opt/warc-indexer/status


Usage: ./warc-indexer.sh [warc|warc-folder]*


Index 2 WARC files:

  ./warc-indexer.sh mywarcfile1.warc.gz mywarcfile2.warc.gz

Index all WARC files in "folder_with_warc_files" (recursive descend) using
20 threads (this will take 20GB of memory):

  THREADS=20 ./warc-indexer.sh folder_with_warc_files

Index all WARC files in "folder_with_warc_files" (recursive descend) using
20 threads and with an alternative Solr as receiver:

  THREADS=20 SOLR_URL="http://ourcloud.internal:8123/solr/netarchive" ./warc-indexer.sh folder_with_warc_files

Note:
Each thread starts its own Java process with -Xmx1024M.
Make sure that there is enough memory on the machine.

Tweaks:
  SOLR_URL:       The receiving Solr end point, including collection
                  Value: http://localhost:8983/solr/netarchivebuilder

  SOLR_CHECK:     Check whether Solr is available before processing
                  Value: true

  SOLR_COMMIT:    Whether a Solr commit should be issued after indexing to
                  flush the buffers and make the changes immediately visible
                  Value: true

  THREADS:        The number of concurrent processes to use for indexing
                  Value: 2

  STATUS_ROOT:    Where to store log files from processing. The log files are
                  also used to track which WARCs has been processed
                  Value: /opt/warc-indexer/status

  TMP_ROOT:       Where to store temporary files during processing
                  Value: /opt/warc-indexer/status/tmp

  INDEXER_JAR:    The location of the warc-indexer Java tool
                  Value: /opt/warc-indexer/warc-indexer-3.3.1-jar-with-dependencies.jar

  INDEXER_MEM:    Memory allocation for each builder job
                  Value: 1024M

  INDEXER_CONFIG: Configuration for the warc-indexer Java tool
                  Value: /opt/warc-indexer/config3.conf

  INDEXER_CUSTOM: Custom command line options for the warc-indexer tool
                  Value: ""
                  Sample: "--collection yearly2020"
```

### Solr

Use the [official image](https://hub.docker.com/_/solr).

To run Solr in kubernetes see [Official Kubernetes operator for Apache Solr](https://github.com/apache/solr-operator).

Previously this repository contained a Dockerfile that built a [Solr](https://solr.apache.org/guide/solr/latest/index.html) container image (based on the official image) with the "netarchivebuilder" configset from the [SolrWayback bundle version 4.4.2](https://github.com/netarchivesuite/solrwayback/releases/tag/4.4.2).

## Docker Compose

See [docker-compose](./docker-compose/).

## TODO

- Kubernetes deployment files and examples.
