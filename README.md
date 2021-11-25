# Teller Sandbox

## Introduction

Sandbox that returns account and transaction data mimicking the same schema as that in production.

## Install

```
$ python -m venv .venv
$ cd .venv/Scripts
$ . activate
$ pip install -r requirements.txt
```

## Run
Navigate to parent directory and execute:
```
$ ./run.sh
```
This will start the server listening on `:8000`. You can now visit [localhost:8000](http://localhost:8000) in your browser and start using the application.

## Usage

Log in into the app with the following credentials: user_XXXXX (5 X's), where X is a digit. 
Use "user_multiple_XXXXX" for user with multiple accounts. Password empty.

Each token will always return the same response.

## Tests
Navigate to test directory and execute:
```
pytest tests.py
```
