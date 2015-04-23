#!/bin/sh

echo "\n----------------------------------------------------------------------"
echo "Running tests without django"
echo "----------------------------------------------------------------------"

nosetests --nocapture

echo "\n----------------------------------------------------------------------"
echo "Running tests with django"
echo "----------------------------------------------------------------------"

python runtests_django.py