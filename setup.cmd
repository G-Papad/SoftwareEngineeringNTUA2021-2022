call python -m venv tl21-75-env
call .\tl21-75-env\Scripts\activate
call python -m pip install -r .\requirements.txt
call python .\tl2175\manage.py runserver
