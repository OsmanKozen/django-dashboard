## Project Setup

```
python -m venv django_dashboard

cd django_dashboard
pip install -r ../requirements.txt

source django_dashboard/bin/activate

cd ..
python manage.py collectstatic
python manage.py runserver
```
