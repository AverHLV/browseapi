#!/bin/bash

echo `echo $SECRET | base64 --decode` > browseapi/tests/secret.json

coverage run -m unittest browseapi.tests.test_client
coverage report
codecov -t $CODECOV_TOKEN
