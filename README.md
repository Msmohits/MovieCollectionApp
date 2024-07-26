# MovieCollectionApp
https://docs.google.com/document/d/1IYGW6CZB5nQ3DmNgBotI10h0bnGep1r5g2D_ZRaFMDc/

## Command used by me

django-admin startproject MovieCollectionApp
cd MovieCollectionApp
django-admin startapp moviecollection
python manage.py runserver
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser 
export username = 'iNd3jDMYRKsN1pjQPMRz2nrq7N99q4Tsp9EY9cM0'
export password='Ne5DoTQt7p8qrgkPdtenTK8zd6MorcCR5vXZIJNfJwvfafZfcOs4reyasVYddTyXCz9hcL5FGGIVxw3q02ibnBLhblivqQTp4BIC93LZHj4OppuHQUzwugcYu7TIC5H1'
pip install --upgrade certifi
black . (for formatting files)
uvicorn MovieCollectionApp.asgi:application --host 0.0.0.0 --port 8000 --reload
             or
python manage.py runserver


run testcases with debugger:-
python -m pdb -m pytest moviecollection/tests/test_collection.py
run all testcase:-
pytest
run specific testcase:-
pytest moviecollection/tests/test_register.py::test_users_view


