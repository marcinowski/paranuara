#!/usr/bin/env bash
##########################################################
# Note the usage of `pwd` instead of `dirname`.          #
# This requires the script to be run from its directory. #
##########################################################

if [ "$(python -c 'import sys; print(sys.version_info[0])')" -lt 3 ]; then
    echo "Incompatible python version. Must be greater than 3."
    return 0
else
    echo "Compatible python version found"
fi

echo "Starting MongoDB server"
# I do it before anything else, so when it's needed it's ready
mongod --dbpath "$(pwd)"/mongodb &
sleep 20
# giving db some time to initiate

if [[ -e "$(pwd)"/venv ]]; then
    echo "Virtualenv directory found."
else
    echo "Virtualenv directory not found."
    pip install virtualenv
    echo "Setting up venv"
    virtualenv venv
fi
echo "Activating venv"
source venv/bin/activate
echo "Installing requirements."
pip install -r requirements.txt
echo "Setting up mongoDB"
mongo < mongo_setup.js
echo "Populating database"
python src/manage.py populate_db
echo "Runserver on port 8000"
python src/manage.py runserver
