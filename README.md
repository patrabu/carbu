# CARBU

Web app to register vehicle gas refills.
It register the mileage, the price and the quantity for a car.

The data is stored in a sqlite3 database.

## Requirements

This web-app is powered by the [flask](http://flask.pocoo.org) python microframework.

The client-side uses [bootstrap](http://getbootstrap.com) for the interface design.

This application implements the MVVM pattern with the help of the [knockoutjs](http://knockoutjs.com) library and [jquery](http://jquery.com).

[simpleStorage](http://www.jstorage.info/) to cache data on the browser side.

## Model

This application uses 3 kind of objects :

A user object, a car object and a refill object.

The user instance is used to identified the api connections.

The car instance describe a vehicle.

The refill instance contains the useful data :
    . datetime when a refill happens
    . mileage, absolute mileage at the moment of the refill
    . quantity, gas quantity put in the tank
    . price paid for the gas refill.

With these data, we can compute the average consumption and price for the refills.

## Quickstart

### Create the virtual environment

Create the virtual directory and populate it with the current version of python :

For Debian (and derivatives):

```shell
pyvenv --withou-pip venv

source venv/bin/activate

curl https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py | python

deactivate
```

For others (?):

```shell
pyvenv --withou-pip venv
```

Install the requirements (from the requirements.txt file):

```shell
source venv/bin/activate

pip install -r requirements.txt
```

### Create the database

Run the script init_db.py with carbu argument :

```shell
# Activate the virtual environment
source venv/bin/activate

# Initialize the DB
python init_db.py carbu
```

It will create a SQLITE3 file named carbu.sqlite.

This database contains 3 tables : USERS, CARS and REFILLS.

### Initialize data

First we need to create à least one user

I didn't provide an interface to create a user so we create it using curl tool.

First lets start the application :

```shell
# Run the app
./run.py
```

In another shell instance, send a request to create a user named _john_ with a password _secret_.
Note that the password will not be store in the DB but a hash of this pasword.

```shell
curl -i -X POST -d '{"username": "john", "password":"secret"}' -H "Content-Type: application/json" http://127.0.0.1:5000/carbu/api/v1.0/users
```

The server should respond something like this :
```
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 27
Location: http://127.0.0.1:5000/carbu/api/v1.0/users/1
Server: Werkzeug/0.9.6 Python/3.4.2
Date: Fri, 24 Oct 2014 11:49:25 GMT

{
  "username": "john"
}
```

