#!/bin/bash

set -eux

flake8 --show-source --statistics --import-order-style=google --putty-ignore='**/test*.py : D101,D102' --putty-auto-ignore flask_access/flask_access.py
nosetests --with-coverage --cover-package=flask_access --with-timer
