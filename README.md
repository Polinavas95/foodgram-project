# Project Title

Application "Grocery Assistant": a site where users can publish their recipes, add others to favorites, subscribe to publications. Service "Shopping List" will allow users to create a list of products from selected recipes.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

What things you need to install the software and how to install them

- Clone the repository;
- Connect JWT token authentication;
- Activate the virtual environment and install all required packages.

### Installing

Activate the virtual environment and install all required packages using the following commands:
```
pip install -r requirements.txt.
```
To generate JWT, include the Simple JWT library: 
```
pip install djangorestframework-simplejwt
``` 
Update the settings file settings.py:
```
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework_simplejwt.authentication.JWTAuthentication',
        ],
    }
```
Update your urls.py routing file:
```
 from rest_framework_simplejwt.views import (
        TokenObtainPairView,
        TokenRefreshView,
    )
    
    urlpatterns = [
        path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ] 
```
Done.
Now you can make a POST request to localhost: 8000 / api / v1 / token / passing the username and password fields. API will return JWT token:
```
 {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU4NzEyODUzNSwianRpIjoiNzRmMDhkOGEwODQ4NGEzYjgyZmM4MDRhMTQ3ZTEyZmIiLCJ1c2VyX2lkIjoxfQ.GW7Obcvy2TWgsEI5lqSx9BC1mxk0WnsywBHrXScs7bI",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTg3MDQyNDM1LCJqdGkiOiI5ZmNjMWE5YTM5NDQ0Y2Q4OWJlOGFlOGRlYWQxNDE0ZSIsInVzZXJfaWQiOjF9.ZkEdzDN5pNgYToDRJq1CKHjIglK1ir1fhnfcXkmziuk"
    } 
```
To refresh the token, send a POST request to the same address, and pass the refresh token in the refresh field.


Example: Get a list of all publications
```
GET/recipes
```
```
application/json
[
 - {
      "id": 0,
      "author": "string",
      "title": "string",
      "duration": "string",
      "text": "string",
      "image": "image",
      "ingredient": "string",
      "slug": "text",
      "pub_date": "2020-04-18T12:04:46z"
    }
]
```
## Running the tests

The project uses a workflow file yamdb_workflow.yaml for automated testing after the git push command.

# go-rest-service-example

![yamdb_workflow](https://github.com/Polinavas95/foodgram-project/workflows/foodgram/badge.svg)

Site
[Foodgram helper](http://84.252.128.68/recipes)

## Deployment

Make sure you are in the same directory where you saved the dockerfile and start building the image. In the command, specify the name of the image: 
```
docker build -t name .
```
The dot at the end of the command is the path to the dockerfile from which to build.
When the build is complete, run the container: 
```
docker run -it -p 8000: 8000 foodgram-project
```
Now you can go in your browser to localhost: 8000, where is your application.

## Built With

* [Django Rest Framework](https://www.django-rest-framework.org/) - The web framework used
* [Docker](https://www.docker.com/) - Software for deploying and managing applications in containerized environments.

## Authors

* **Vasileva Polina** - [VK](https://vk.com/id36439980)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Don't be afraid to try new things
* Learn interesting
