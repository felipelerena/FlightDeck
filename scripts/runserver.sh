#!/bin/bash

source scripts/environment.sh

# run server
cd $PROJECT_DIR/$PROJECT_NAME/
$PYTHON_COMMAND ./manage.py runserver localhost:8090 --adminmedia=$PROJECT_DIR/$PROJECT_NAME/adminmedia/
