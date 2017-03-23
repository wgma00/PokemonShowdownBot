#!/bin/bash
DNF_CMD=$(which dnf)
APT_GET_CMD=$(which apt-get)
PIP_CMD=$(which pip)
# install the relevant pip manager if it's not installed
if [[ -z ${PIP_CMD} ]]; then
    wget https://bootstrap.pypa.io/get-pip.py
    python3 get-pip.py
    echo "pip installed for python3"
else
    echo "pip already installed"
fi
echo "Installing pip dependacies to run PokemonShowdownBot"
pip install -r requirements.txt
# install the required libraries for latex
# related libraries and calculator related libraries
echo "Installing relevant Linux modules"
if [[ ! -z ${DNF_CMD} ]]; then
    dnf install gnome-calculator
    dnf install texlive
    dnf install poppler-utils
elif [[ ! -z ${APT_GET_CMD} ]]; then
    apt-get install texlive-latex-recommended
    apt-get install texlive-latex-extra
    apt-get install poppler-utls
    apt-get install gnome-calculator
fi
