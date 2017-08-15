@ECHO OFF
cd %~dp0
IF NOT EXIST %~dp0\venv (
    echo Virtualenv directory not found.
    pip install virtualenv 1> nul
    echo Setting up venv.
    virtualenv venv 1> nul
) ELSE (
    echo Virtualenv directory found.
)
echo Setting up mongoDB
REM I do it before pip install, so it initiates in the background
mongo < mongo_setup.js
start /b mongod --dbpath %~dp0\mongodb 1> nul
echo Activating virtualenv.
start venv/Scripts/activate
echo Installing requirements.
pip install -r requirements.txt
cd src
echo Populating database
python manage.py populate_db
echo Runserver on port 8000
python manage.py runserver
