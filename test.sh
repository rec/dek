#!/bin/bash

set -eux

mypy dek
isort dek test_dek.py
black dek test_dek.py
ruff check --fix dek test_dek.py
coverage run $(which pytest)
coverage html
