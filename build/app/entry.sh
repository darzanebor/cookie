#!/bin/bash
gunicorn -u `id -u` -g `id -g` --threads=1 --workers=2 --log-config=gunicorn_logging.conf --worker-connections="${COOKIE_WORKER_CONN:-500}" --bind="${COOKIE_HOST:-0.0.0.0}:${COOKIE_PORT:-5000}" main:application
