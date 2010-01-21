#!/bin/bash

# activate Python flightdeck environment
cd $PYTHON_ENVIRONMENTS_DIR
source $PYTHON_ENVIRONMENT/bin/activate

# set path to the project direcotry
PYTHONPATH=$PROJECT_DIR:$PYTHONPATH
