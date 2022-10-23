You should run the project as follows:

cd 'your_project_folder'
python3 -m venv django_dashboard

cd django_dashboard
pip3 install -r ../requirements.txt

cd ..
source django_dashboard/bin/activate

python manage.py runserver