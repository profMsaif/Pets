# Pets Records

## Description
 project keep a record for pets such as cats and dogs
## run test
```
   $ docker-compose run web python manage.py test 
```
or you can add python manage.py test to the command
for web service
```
    python manage.py test
```
# create env variables
    the env variables can be found in env.example
    create .env file  for you env and set them
    carefully.
    - in order for to have and api_key  you must generate your own
     with any string generator and add to API_KEY variable 

    - set PROJECT_DEBUG to False in the production env 

## deploy
- make sure that your server have both docker and docker-compose

```
    $ git clone https://github.com/profMsaif/Pets.git
    $ cd Pets
```
- copy env.example into .env and add your own values 
```
    $ cp env.example .env
```
then run:
```
    $ docker-compose up --build -d
```
# deploy 
- deploy on heroku: coming soon
- deploy on aws: coming soon
