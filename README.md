# central_hub

## 1. About
This repository contains the script that will be ran on the central hub. The main function of the central hub includes:
  - Adding peripheral devices to the network
  - Collecting distance measurements from the peripheral
  - Sending collected data to the database

## 2. Setup
To set up the central hub dependencies and run within a virtualenv, run these commands:
  - "pip3 install virtualenv"
  - "virtualenv \<env\>"
  - "source ./\<env\>/bin/activate"
  - "pip install -r requirements.txt"
  
If you don't want to run in a virtualenv, just run the last command to install the requirements. 

Next, download the Google Cloud Project authentication file. To set the authentication file, use the following command:
  - "export GOOGLE_APPLICATION_CREDENTIALS="~/\<auth_json\>"

Now, you will be able to run the script.
