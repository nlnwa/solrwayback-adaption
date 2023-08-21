To test solrwaybak in minikube

run ``` kubectl apply -k . ``` from this directory,

then mount local directory that contains WARC files with

``` minikube mount /path/to/warc/files:/data/warcs/ ```

Start warc-indexer by running ```kubectl apply -k . ``` from /deploy/dev/warc-indexer

Restart solrwayback pod to see the indexed files.
