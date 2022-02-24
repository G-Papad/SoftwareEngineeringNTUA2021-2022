call .\tl21-75-env\Scripts\activate
call cd ./tl2175
start python .\manage.py runserver
start chrome http://127.0.0.1:8000/interoperability/api
start cmd /k "TITLE ConnectWays_CLI" 