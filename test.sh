#!/bin/bash
if [[ ! -z `pip3 list | grep pytest` ]]; then
	python3 -m pytest test --pep8
else
	echo "Pytest is not installed for python3. Install by executing install.sh"
fi
