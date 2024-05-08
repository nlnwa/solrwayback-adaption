# Run SolrWayabck using Docker Compose

> Note: The following also works with `podman compose up`.

## 1. Create and populate a volume with WARC files

```shell
# Create a volume called "warcs"
docker create volume warcs

# Populate the "warcs" volume with files
docker run --rm -v /path/to/my/warcs:/source:Z  -v warcs:/target busybox sh -c "cp -r /source/* /target"
```

### Alternatively bind mount a volume with WARC files

If you don't want to create and populate a volume another option is to bind mount the "warcs" volume from a local directory:

```yaml
# compose.yaml

volumes:
  warcs:
    # external: true
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /path/to/my/warcs
```

> Bind mounting a volume can lead to permisssion issues and depends on the container user having permission to read the files mounted on the host.

## 2. Run docker compose

```shell
docker-compose up
```

The following steps are performed:

1. Start solr in cloud mode (with embedded zookeeper).
2. Wait for solr to be ready.
3. Create a solr configset named "solrwayback".
4. Create a solr collection named "solrwayback"
5. Index files in the "warc" volume to the Solr "solrwayback" collection.

## 3. Open SolrWayback

### Solrwayback UI

[http://localhost:8080/solrwayback](http://localhost:8080/solrwayback)

### Solr Admin UI

[http://localhost:8983/solr](http://localhost:8983/solr)
