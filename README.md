
# WallApp - Backend

This is a simple API built with `python3`, `django`, `django-rest-framework`, and `dj-rest-auth`.

This API contains two entities (`user` and `post`) and provides the necessary methods to handle basic **CRUD** (create, read, update and delete) operations and user authentication/registration.

The front-end application can be found [here](https://github.com/lucas-caribe/wallapp-frontend).

## Requirements

- python 3.8
- pip
- pipenv

## Installation

Start by cloning this repository
```bash
git clone git@github.com:lucas-caribe/wallapp-backend.git
cd wallapp-backend
```
After cloning the repository, make sure python 3.8 is installed on your computer.

```bash
python3 --version
```

Install the packaging tool `pipenv`
```bash
pip3 install pipenv
```
Install the project dependencies and start the shell
```bash
pipenv install
pipenv shell
```
This project uses the sendgrid API for sending emails after registration. Therefore, before starting the server, it is important that you create a `.env` file containing the following variables:

```
SENDGRID_API_KEY = <your_key_here>
FROM_EMAIL = <your_sender_email>
```
## Unit Testing

You can run the tests created for this application by running the command
```bash
python3 manage.py test
```
And you can check the test coverage by running
```bash
coverage run manage.py test
coverage report
```
## Usage

First you need to get the server running
```bash
python3 manage.py runserver
```
Then you can try all the functionalities of this API by using an 'API Client' such as `Insomnia` or `Postman`.

This API is designed to be used by this front-end application [here](https://github.com/lucas-caribe/wallapp-frontend). So you can also consider installing and running it if you want to see how everything works together.
