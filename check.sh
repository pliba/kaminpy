#!/bin/bash
clear
set -e
mypy "$1".py
pytest -qq `basename "$1" .py`_test.py
flake8 "$1".py `basename "$1" .py`_test.py
