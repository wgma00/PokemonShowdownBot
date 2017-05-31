#!/bin/bash


install_dep_apt() {
    apt-get install texlive-full
    apt-get install texlive-pictures
    apt-get install poppler-utils
    # might not be installed on some systems with poppler-utils
    apt-get install pnmtopng
    # gnome-calculator package was formally known as gcalctool on earlier
    # versions like ubuntu 12.04
    if [[ -z `apt-cache search gnome-calculator` ]]; then
        apt-get install gcalctool
    else
        apt-get install gnome-calculator
    fi
}

install_dep_dnf() {
    dnf install gnome-calculator
    dnf install texlive
    dnf install poppler-utils
}


DNF_CMD=`which dnf`
APT_GET_CMD=`which apt-get`
PIP_CMD=`which pip`

# prompting for sudo 
if [ $EUID != 0 ]; then
    sudo "$0" "$@"
    exit $?
fi


# install the relevant pip manager if it's not installed
if [[ -z PIP_CMD ]]; then
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
if [[ ! -z $DNF_CMD ]]; then
    install_dep_dnf
elif [[ ! -z $APT_GET_CMD ]]; then
    install_dep_apt
fi
