#!/bin/bash

# export graphical model representation to given file
# example: 
# ./scripts/graphviz.sh ../Docs/models.png
# to get all models used within applications:
# ./scripts/manage.py graph_models jetpack person base amo -g -o ../Docs/all_models.png

source scripts/environment.sh

# run server
cd $PROJECT_DIR/$PROJECT_NAME/
$PYTHON_COMMAND ./manage.py graph_models jetpack person base amo -g -o $1
