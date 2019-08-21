#!/bin/bash

coverage run -m unittest browseapi.tests.test_client
coverage report

codecov -t $CODECOV_TOKEN
