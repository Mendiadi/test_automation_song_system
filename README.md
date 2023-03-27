# Test Automation for song system

## overview:
in this project im tested the song server
api's, im wrote the automation using pytest
and requests packages, report using allure.
* also have unit tests to some functionality notice that 


## how to run:
make sure you have the requirements installed
```commandline
   pipenv install
```
```commandline
    pipenv shell
```
or 
```commandline
    pip install -r requirements
```
### make sure you installed allure package
### otherwise tests will not run...
allure install guide - todo

## run options:
to run all tests with reports:
```commandline
    pytest
```
run with cli args:
you can insert host and port by cli like:
```commandline
    pytest --host http://127.1.1.0
    pytest --port 3002
```
of course you can combain all args and markers in one call

run with markers :
```commandline
    pytest -m users
    pytest -m playlists
    pytest -m songs
    pytest -m general
```
by default pytest ignore 15 tests of the unit tests
if you want to run only the unit test (im don't know why you should but anyway)
```commandline
    pytest -m unit
```

## reports
to run and see the reports 
```commandline
    allure serve reports
```
