#!/bin/sh

set -e

if [ -z $NGINX_USER ]; then
  echo >&2 "NGINX_USER must be set"
  exit 1
fi

if [ -z $NGINX_PASSWORD ]; then
  echo >&2 "NGINX_PASSWORD must be set"
  exit 1
fi

htpasswd -bBc /etc/nginx/.htpasswd $NGINX_USER $NGINX_PASSWORD

exec nginx -g "daemon off;"