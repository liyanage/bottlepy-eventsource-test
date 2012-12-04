#!/bin/sh


server_type=$1

if [ -z $server_type ]; then
	echo Usage: $0 'server_name'
	echo Server name is one of wsgiref, paste, rocket, waitress, cherrypy
	exit 1
fi

echo server type: $server_type

PYTHONPATH=lib/Rocket-src-1.2.4.zip:lib/waitress-master.zip/waitress-master:lib/CherryPy-3.2.2.zip/CherryPy-3.2.2:lib/Paste-1.7.5.1.zip/Paste-1.7.5.1:lib/bottle-master.zip/bottle-master ./generatortest.py $server_type



