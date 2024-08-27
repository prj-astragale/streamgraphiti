#!/bin/bash

# set -ex

# export SIMPLE_SETTINGS=settings
# $WORKER worker --web-port=$WORKER_PORT

faust -A app.main worker -l info