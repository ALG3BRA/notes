# Notes
## Docs
You can read the documentation of the routes in Postman:
([Postman Collection](https://www.postman.com/alg3bra/ec178037-915d-4d52-bc8c-11f69b2d814b/request/pp25avu/register))

## Running application (Docker)
to run the main application run: 
```
docker-compose up -d --build
```
to run the testing mode run:
```
docker-compose -f ./docker-compose-test.yml up -d --build
```
then you can see backend logs in interactive mode by running this command:
```
docker logs -f app
```
to kill application run:
```
docker-compose down
```

## Pre-commit (Black)
```
pip install pre-commit
```
Just run this command before starting to do git commits 
