# FrieghtFox POC

## How to use:

Note: 
Api Keys have been ignored from addition please add them before deploying.
The directory is as follows: assignment/utils/api_key.py

move to frieghtfox repo where the docker-compose.yaml is present and run below command

```docker-compose up -d```

to test the service run the below command in browser window

```http://127.0.0.1:8000/weather/?date=2024-02-24&pincode=560048```

Note: Used the current weather external API as historical and forecast API's were paid. The entered date is taken into consideration for caching but weather will be inaccurate for the first fetch call.
