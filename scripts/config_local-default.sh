#!/bin/bash

source scripts/config.sh

PYTHON_ENVIRONMENT=$PROJECT_NAME
PYTHON_COMMAND='python'
# define directories
PYTHON_ENVIRONMENTS_DIR='/srv/python-environments'
PROJECT_DIR=`pwd`
V_ENV=$PYTHON_ENVIRONMENTS_DIR/$PYTHON_ENVIRONMENT
