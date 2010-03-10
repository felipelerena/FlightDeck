#!/bin/bash

BASEDIR=`dirname $0`
source $BASEDIR/config_local.sh
# activate Python flightdeck environment
#cd $PYTHON_ENVIRONMENTS_DIR
source $V_ENV/bin/activate

# set path to the project direcotry
PYTHONPATH=$PROJECT_DIR/$PROJECT_NAME:$PROJECT_DIR:$PYTHONPATH

# cuddlefish env
CUDDLEFISH_ROOT="$V_ENV"
export CUDDLEFISH_ROOT
