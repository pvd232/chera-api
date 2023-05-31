# 🚀 Welcome to Chera!

# ------> Setup Instructions <------

# ------> Pre-installation Requirements

# 1. Python version 3.11.0 must be installed on your machine and added as a PATH variable (find an online article to do this). If you are using a macbook, make sure you have seperately installed Python 3.11.0, as the default version that comes preinstalled is Python 2. You can test your installation by entering "which python3" into your terminal, and it should print out the location of Python on your machine. Make sure the version is 3.11

# 2. PostgreSQL version 14.1.0 must be installed on your machine and added as a PATH variable, you can test this by entering "which psql" into your terminal, and it should print out the location of PostgreSQL on your machine

# 3. You must have Github integrated with your Editor, and must be logged in. Git must also be added as a path variable. To test this, enter "which git" into your terminal. Same thing as Python.

# ------> Initial Project Set Up Instructions (OSX, if using Windows, look up the equivalent powershell commands)

# Python setup

# 1. Go to your terminal, navigate to the "flask-server" directory

# 2. Enter the following command to create a python virtual environment named "venv" for the project "python3 -m venv venv"

# 3. While still in the flask-server directory, enter the following command to activate your python virtual environment "source ./venv/bin/activate". You should now see a "(venv)" to the left of your computer name in your console

# 4. Enter "cd.." into your terminal to navigate to the bendito-api directory, which is the parent directory of flask-server and the root directory of the backend

# 5. Enter "pip install -r requirements.txt" into your terminal to install the project python dependencies into the venv folder

# PSQL setup

# 1. Go to your terminal and enter "psql" to begin a PostgreSQL session

# 2. Enter the following psql command to create a local version of the project database "create database nourishdb;"

# 3. Confirm creation by entering "\l" into your terminal. The database nourishdb should be listed.

# 4. Start the backend by opening the "main.py" file and running it. you should see a message in your console confirming successful startup.

# 5. Input the following url into your browser "localhost:4000/api/setup_tables" and hit enter. This will instantiate the database's tables that are listed in models.py

# 6. Confirm successful setup by going back to the terminal window with psql running, and enter the following command "\c nourishdb". You should receive a confirmatory message saying you have connected to the database

# 7. Enter "\dt" into your terminal. A list of tables should print out. This confirms successful setup.

# ------> Continuous Setup Instructions <------

# 1. Depending on your editor (VSCode is highly reccomended) you might have to manually activate the virtual env periodically. You can see if it is activated by checking for the (venv) in your console

# 2. To start the backend, run main.py in your editor

# 3. When signing off, shut down the backend by entering "ctrl + c" into the terminal window that has the backend running
