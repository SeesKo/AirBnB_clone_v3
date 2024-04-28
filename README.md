# AirBnB clone - RESTful API

This is the third segment of the AirBnB project at Holberton School that will collectively cover fundamental concepts of higher level computer programming. The goal of the AirBnB project is to eventually set up a server that runs a simple replica of the AirBnB Website(HBnB). A command line interpreter is created in this segment to manage objects for the AirBnB(HBnB) website.

#### Functionalities of this command interpreter:
* Creates a new object (ex: a new User or a new Place).
* Retrieves an object from a file, a database etc...
* Does operations on objects (count, compute stats, etc...).
* Updates attributes of an object.
* Destroys an object.

## Table of Contents
* [Environment](#environment)
* [Installation](#installation)
* [File Descriptions](#file-descriptions)
* [Usage](#usage)
* [Examples of use](#examples-of-use)
* [Bugs](#bugs)
* [Authors](#authors)
* [License](#license)

## Project Requirements

### Python Scripts

- All files will be interpreted/compiled on Ubuntu 20.04 LTS using `python3` (version 3.4.3).
- Code should use the `PEP 8` (version 1.7).
- All files must be executable.
- All modules should have documentation (`python3 -c 'print(__import__("my_module").__doc__)'`)
- All classes should have documentation (`python3 -c 'print(__import__("my_module").MyClass.__doc__)'`)
- All functions (inside and outside a class) should have documentation `(python3 -c
    -'print(__import__("my_module").my_function.__doc__)' and python3 -c
    -'print(__import__("my_module").MyClass.my_function.__doc__)'`)

### Python Unit Tests

- All tests should be executed by using this command: `python3 -m unittest discover tests`.
- Individual test files can also be tested by using this command: `python3 -m unittest tests/test_models/test_base_model.py`.

## Examples of use
```
vagrantAirBnB_clone$./console.py
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  all  create  destroy  help  quit  show  update

(hbnb) all MyModel
** class doesn't exist **
(hbnb) create BaseModel
7da56403-cc45-4f1c-ad32-bfafeb2bb050
(hbnb) all BaseModel
[[BaseModel] (7da56403-cc45-4f1c-ad32-bfafeb2bb050) {'updated_at': datetime.datetime(2017, 9, 28, 9, 50, 46, 772167), 'id': '7da56403-cc45-4f1c-ad32-bfafeb2bb050', 'created_at': datetime.datetime(2017, 9, 28, 9, 50, 46, 772123)}]
(hbnb) show BaseModel 7da56403-cc45-4f1c-ad32-bfafeb2bb050
[BaseModel] (7da56403-cc45-4f1c-ad32-bfafeb2bb050) {'updated_at': datetime.datetime(2017, 9, 28, 9, 50, 46, 772167), 'id': '7da56403-cc45-4f1c-ad32-bfafeb2bb050', 'created_at': datetime.datetime(2017, 9, 28, 9, 50, 46, 772123)}
(hbnb) destroy BaseModel 7da56403-cc45-4f1c-ad32-bfafeb2bb050
(hbnb) show BaseModel 7da56403-cc45-4f1c-ad32-bfafeb2bb050
** no instance found **
(hbnb) quit
```

## Bugs
No known bugs at this time. 

## Authors
Alexa Orrico - [Github](https://github.com/alexaorrico) / [Twitter](https://twitter.com/alexa_orrico)  
Jennifer Huang - [Github](https://github.com/jhuang10123) / [Twitter](https://twitter.com/earthtojhuang)

- Second part of Airbnb: Joann Vuong
- Third part of Airbnb: Erick Siiko

## License
All Rights Reserved.
