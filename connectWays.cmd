call .\tl21-75-env\Scripts\activate
start python .\tl2175\manage.py runserver_plus --cert-file .\tl2175\cert.pem --key-file .\tl2175\key.pem
start https://127.0.0.1:8000/interoperability/api
start cmd /k "TITLE ConnectWays_CLI"
