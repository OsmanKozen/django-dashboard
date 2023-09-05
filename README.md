## Technology Stack

asgiref==3.5.2
certifi==2022.6.15
cffi==1.15.1
charset-normalizer==2.1.1
cx-Oracle==8.3.0
Django==3.2.15
django-cleanup==8.0.0
django-crispy-forms==1.14.0
django-import-export==2.8.0
django-multiselectfield==0.1.12
django-python3-ldap==0.15.3
et-xmlfile==1.1.0
h5py==3.7.0
html5lib==1.1
idna==3.3
Jinja2==3.1.2
MarkupPy==1.14
MarkupSafe==2.1.1
numpy==1.21.6
odfpy==1.4.1
openpyxl==3.0.10
pandas==1.3.5
pycparser==2.21
pyflakes==2.5.0
pyparsing==3.0.9
python-dateutil==2.8.2
pytz==2022.2.1
PyYAML==6.0
requests==2.28.1
six==1.16.0
sqlparse==0.4.2
tablib==3.2.1
typing-extensions==4.3.0
urllib3==1.26.12
webencodings==0.5.1
xlrd==2.0.1
xlwt==1.3.0
python-decouple==3.6
whitenoise==6.5.0

## Project Setup

```
python -m venv django_dashboard

cd django_dashboard
pip install -r ../requirements.txt

source django_dashboard/bin/activate

cd ..
python manage.py runserver
