FROM docker.io/alpine:latest as build

RUN apk add --no-cache zip
WORKDIR /tmp
COPY conf conf
RUN cd conf && zip -r /tmp/configset.zip *


FROM quay.io/curl/curl:latest
COPY --from=build /tmp/configset.zip /tmp/configset.zip
