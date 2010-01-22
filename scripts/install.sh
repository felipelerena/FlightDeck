#!/bin/bash

# copy configuration files to local 
for loc in flightdeck/*_local-default.py
do
	if [ -e flightdeck/`basename $loc "-default.py"`.py ]
	then 
		echo file exists flightdeck/`basename $loc "-default.py"`.py
	else 
		cp $loc flightdeck/`basename $loc "-default.py"`.py
		echo $loc "->" flightdeck/`basename $loc "-default.py"`.py
	fi
done

for wsgi in apache/*_local-default.wsgi
do
	if [ -e apache/`basename $wsgi "-default.wsgi"`.wsgi ]
	then 
		echo file exists apache/`basename $wsgi "-default.wsgi"`.wsgi
	else 
		cp $wsgi apache/`basename $wsgi "-default.wsgi"`.wsgi
		echo $wsgi "->" apache/`basename $wsgi "-default.wsgi"`.wsgi
	fi
done

for sh in scripts/*_local-default.sh
do
	if [ -e scripts/`basename $sh "-default.sh"`.sh ]
	then 
		echo file exists scripts/`basename $sh "-default.sh"`.sh
	else
		cp $sh scripts/`basename $sh "-default.sh"`.sh
		echo $sh "->" scripts/`basename $sh "-default.sh"`.sh
	fi
done

# force exclude local files
cp tools/git-exclude .git/info/exclude
echo tools/git-exclude "->" .git/info/exclude
