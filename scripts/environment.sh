#!/bin/bash

source scripts/config_local.sh
# activate Python flightdeck environment
#cd $PYTHON_ENVIRONMENTS_DIR
source $V_ENV/bin/activate

# set path to the project direcotry
PYTHONPATH=$PROJECT_DIR/$PROJECT_NAME:$PROJECT_DIR:$PYTHONPATH
