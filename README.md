## Instructions
1. Set your variables in the .env file
 
2. $ docker compose up -d 
A Nginx container will get created, with a port mapping of 3333:80

Now we can check that we can read the file using:
3. $ curl -X POST "http://localhost:3333/api" -H 'Content-Type: application/json' -d'
{
    "isDb": false
}'

If we want to move the file to the "done" directory, and also write its content to the DB:
4. $ curl -X POST "http://localhost:3333/api" -H 'Content-Type: application/json' -d'
{
    "isDb": true
}'
