#!/bin/bash
if [[ ! -z `pip3 list | grep pytest` ]]; then
	python3 -m pytest test
else
	echo "Pytest is not installed for python3. Install by executing install.sh"
fi
