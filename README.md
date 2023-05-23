## Instructions
1. Set your variables in the .env file
2. $ docker compose up -d
3. $ curl -X POST "http://localhost:3333/api" -H 'Content-Type: application/json' -d'
{
    "isDb": false
}'
4. $ curl -X POST "http://localhost:3333/api" -H 'Content-Type: application/json' -d'
{
    "isDb": true
}'
