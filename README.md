# Project Name
simple django vue project

## Installation
### backend
Specify the license type.
mkdir backend
create requirements.txt
python -m venv venv
venv/Scripts/Activate
pip install -r requirements.txt
django-admin startproject config .
python manage.py startapp propertycontrol
python manage.py makemigrations
python manage.py migrate
python manage.py runserver


### frontend
npm create vue@latest
name project frontend
cd .\frontend\
npm install
npm install vue-router@4
npm run dev