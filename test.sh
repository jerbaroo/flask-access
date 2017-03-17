#!/bin/bash

set -eux

./venv/bin/flake8 --show-source --statistics --import-order-style google flask_access/flask_acces.py
./venv/bin/nosetests --with-coverage --cover-package=flask_access --with-timer
