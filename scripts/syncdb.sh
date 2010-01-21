#!/bin/bash

source scripts/config_local.sh
source scripts/environment.sh

# run server
cd $PROJECT_DIR/flightdeck/
$PYTHON_COMMAND ./manage.py syncdb

