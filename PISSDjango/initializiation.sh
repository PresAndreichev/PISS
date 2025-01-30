#!/bin/bash

# NB - the script needs to be sourced into current terminal with 'source initialization_script.sh' and the sudo password be given

# Install the system (OS) dependencies
sudo apt update && sudo apt upgrade -y

# Gcc, CMake
sudo apt install build-essential -y
# Install Python and also add an alias to use with python command
sudo apt install python3 -y

# Add this line to your ~.bashrc file for persistent alias - maybe refactor later to check if the line exists and if not, to add it to the user's profile
alias python='python3'


sudo apt install python3-venv -y
sudo apt install python3-dev -y

# For generating the diagrams, we need some more external dependancies
sudo apt install graphviz -y
sudo apt install libgraphviz-dev pkg-config -y
sudo apt install graphviz-dev -y

# Create the virtual environment if one doesn't already exist
if [ ! -d './venv' ]; then
    python3 -m venv ./venv
fi
# Run it for the UNIX-based systems
source ./venv/bin/activate
# Install the dependencies for the project
pip install --upgrade pip
pip install -r requirements.txt 
