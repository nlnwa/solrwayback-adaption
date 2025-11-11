FROM docker.io/alpine:latest AS build

RUN apk add --no-cache zip
WORKDIR /tmp
COPY conf conf
RUN cd conf && zip -r /tmp/configset.zip *


FROM docker.io/curlimages/curl:8.17.0
COPY --from=build /tmp/configset.zip /tmp/configset.zip
