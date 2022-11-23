#!/bin/bash

OPTION="$1"

if [[ $OPTION == "api" ]]; then
	nosetests tests/test_api.py > tests/results/api.txt 2>&1

elif [[ $OPTION == "users" ]]; then
	nosetests tests/test_users.py > tests/results/users.txt 2>&1

elif [[ $OPTION == "tasks" ]]; then
	nosetests tests/test_tasks.py > tests/results/tasks.txt 2>&1

elif [[ $OPTION == "main" ]]; then
	nosetests tests/test_main.py  > tests/results/main.txt 2>&1

elif [$OPTION="all"]; then
	nosetests --with-coverage --cover-erase --cover-package=project > results.txt  2>&1

fi