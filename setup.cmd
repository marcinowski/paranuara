@ECHO OFF
cd %~dp0
IF NOT EXIST %~dp0\venv (
    echo Virtualenv directory not found.
    pip install virtualenv
    echo Setting up venv.
    virtualenv venv
) ELSE (
    echo Virtualenv directory found.
)
echo Activating virtualenv.
start venv/Scripts/activate
echo Installing requirements.
pip install -r requirements.txt
echo Setting up mongoDB
mongo < mongo_setup.js
start /b mongod --dbpath %~dp0\mongodb
cd src
echo Populating database
python manage.py populate_db
echo Runserver on port 8000
python manage.py runserver
