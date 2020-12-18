#!/bin/bash

set -eux

(cd flask_access && flake8 --show-source --statistics\
  --import-order-style=google\
  --per-file-ignores='test*.py:D101,D102,E731')
python3 -m "nose" --with-coverage --cover-package=flask_access --with-timer
