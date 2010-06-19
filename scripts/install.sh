#!/bin/bash

source scripts/config_local.sh

### PIP packages installation
export PYTHONPATH=
pip install -E $V_ENV/ -r $PROJECT_DIR/tools/pip-requirements.txt

# src dir
SRC=$V_ENV/src
# find last python dir
for i in $V_ENV/lib/python*
do
	SITE_PACKAGES=$i/site-packages
done

### upload dir 
if [ ! -e $PROJECT_DIR/upload/ ]
then
	mkdir $PROJECT_DIR/upload/
fi

### flightdeck media dir 
if [ ! -e $PROJECT_DIR/$PROJECT_NAME/media/ ]
then
	mkdir $PROJECT_DIR/$PROJECT_NAME/media/
fi

### link tutorial application 
if [ ! -e $PROJECT_DIR/$PROJECT_NAME/media/tutorial ]
then
	ln -fs $PROJECT_DIR/$PROJECT_NAME/tutorial/media/ $PROJECT_DIR/$PROJECT_NAME/media/tutorial
fi


### link jetpack application 
if [ ! -e $PROJECT_DIR/$PROJECT_NAME/media/jetpack ]
then
	ln -fs $PROJECT_DIR/$PROJECT_NAME/jetpack/media/ $PROJECT_DIR/$PROJECT_NAME/media/jetpack
fi

### adminmedia dir
if [ ! -e $PROJECT_DIR/$PROJECT_NAME/adminmedia ]
then
	ln -fs $SITE_PACKAGES/django/contrib/admin/media/ $PROJECT_NAME/adminmedia
fi

### link api application 
if [ ! -e $PROJECT_DIR/$PROJECT_NAME/media/api ]
then
	ln -fs $PROJECT_DIR/$PROJECT_NAME/api/media/ $PROJECT_DIR/$PROJECT_NAME/media/api
fi

### Roar
cd $V_ENV/lib/
if [ ! -e $V_ENV/lib/Roar1.0 ]
then 
	mkdir Roar1.0
	cd Roar1.0
	wget http://digitarald.de/project/roar/1-0/source/Roar.js
	wget http://digitarald.de/project/roar/1-0/assets/Roar.css
	rm $V_ENV/lib/Roar
	ln -fs $V_ENV/lib/Roar1.0 $V_ENV/lib/Roar
fi
if [ ! -e $PROJECT_DIR/$PROJECT_NAME/media/roar ]
then
	ln -fs $V_ENV/lib/Roar/ $PROJECT_DIR/$PROJECT_NAME/media/roar
fi


### Bespin installation
cd $V_ENV/lib/
if [ ! -e $V_ENV/lib/BespinEmbedded-DropIn-0.6.3 ]
then
	wget http://ftp.mozilla.org/pub/mozilla.org/labs/bespin/Embedded/BespinEmbedded-DropIn-0.6.3.tar.gz --no-check-certificate
	tar xfvz BespinEmbedded-DropIn-0.6.3.tar.gz
	rm BespinEmbedded-DropIn-0.6.3.tar.gz
	rm $V_ENV/lib/BespinEmbedded
	ln -fs $V_ENV/lib/BespinEmbedded-DropIn-0.6.3/ $V_ENV/lib/BespinEmbedded
	rm $PROJECT_DIR/$PROJECT_NAME/media/bespin
fi
if [ ! -e $PROJECT_DIR/$PROJECT_NAME/media/bespin ]
then
	ln -fs $V_ENV/lib/BespinEmbedded/ $PROJECT_DIR/$PROJECT_NAME/media/bespin
fi

### CodeMirror installation
# deprecated
#if [ ! -e $V_ENV/src/CodeMirror-0.66 ]
#then 
#	cd $V_ENV/src/
#	wget http://marijn.haverbeke.nl/codemirror/codemirror.zip
#	unzip -x codemirror.zip
#	rm codemirror.zip
#	if [ -e $V_ENV/lib/codemirror ]
#	then 
#		rm $V_ENV/lib/codemirror
#	fi
#fi
#if [ ! -e $V_ENV/lib/codemirror ]
#then
#	ln -fs $V_ENV/src/CodeMirror-0.66/ $V_ENV/lib/codemirror
#fi

#if [ ! -e $PROJECT_DIR/$PROJECT_NAME/media/codemirror ]
#then
#	ln -fs $V_ENV/lib/codemirror $PROJECT_DIR/$PROJECT_NAME/media/codemirror
#fi

### Jetpack SDK
if [ ! -e $V_ENV/src/jetpack-sdk ]
then
	cd $V_ENV/src
	hg clone http://hg.mozilla.org/labs/jetpack-sdk/
	# link necessary execution files
	ln -fs $V_ENV/src/jetpack-sdk/bin/cfx $V_ENV/bin/cfx
	ln -fs $V_ENV/src/jetpack-sdk/bin/jpx $V_ENV/bin/jpx
	ln -fs $V_ENV/src/jetpack-sdk/bin/quick-start $V_ENV/bin/quick-start
	# link packages
	ln -fs $V_ENV/src/jetpack-sdk/packages $V_ENV/packages
	# link libs unable to install via pip
	ln -fs $V_ENV/src/jetpack-sdk/python-lib/cuddlefish $SITE_PACKAGES/cuddlefish
	ln -fs $V_ENV/src/jetpack-sdk/python-lib/ecdsa $SITE_PACKAGES/ecdsa
	# link static files
	ln -fs $V_ENV/src/jetpack-sdk/static-files $V_ENV/static-files
fi


### Grappelli section
# checkout the repository
# TODO: wait with grappelli for the newer Django
#svn checkout http://django-grappelli.googlecode.com/svn/trunk/grappelli/ $SRC/django-grappelli
# link to site-packages
#if [ ! -e $SITE_PACKAGES/grappelli ]
#then
#	ln -fs $SRC/django-grappelli $SITE_PACKAGES/grappelli
#fi
# link adminmedia within project
#if [ ! -e $PROJECT_DIR/$PROJECT_NAME/adminmedia ]
#then
#	ln -fs $SRC/grappelli/media $PROJECT_DIR/$PROJECT_NAME/adminmedia
#fi
