call .\tl21-75-env\Scripts\activate
start python .\tl2175\manage.py runserver
start chrome http://127.0.0.1:8000/interoperability/api
start cmd /k "TITLE ConnectWays_CLI"