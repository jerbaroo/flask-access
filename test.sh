#!/bin/bash

set -eux

flake8 --show-source --statistics --import-order-style google flask_access/flask_access.py
nosetests --with-coverage --cover-package=flask_access --with-timer
