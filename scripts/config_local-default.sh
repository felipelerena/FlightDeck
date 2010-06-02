#!/bin/bash

BASEDIR=`dirname $0`
source $BASEDIR/config.sh

PYTHON_ENVIRONMENT=$PROJECT_NAME
PYTHON_COMMAND=python

# define directories
PROJECT_DIR='/path/to/FlightDeck'
V_ENV=$PROJECT_DIR/flightdeckenv

# that's for graphviz
export TMP=/tmp/
