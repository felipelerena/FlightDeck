#!/bin/bash

source scripts/environment.sh

# run server
cd $PROJECT_DIR/$PROJECT_NAME/
django-admin.py $@
