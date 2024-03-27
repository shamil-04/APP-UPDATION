import os

BASE=os.path.expanduser('~')+"/projects/app/"

LATEST_VERSION="2.0.0"
APP_NAME="hello_log_app"
APP_PATH=os.path.join(BASE,"usr/bin")

UPDATE_NAME=APP_NAME+"-"+LATEST_VERSION
TAR_SRC=os.path.join(BASE,"projects/updater/")+UPDATE_NAME+".tar"
TAR_DEST="/tmp/"+UPDATE_NAME+".tar"
TAR_MD5="12345678"


print(APP_PATH)