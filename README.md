# 2022 SKCS HACKATHON TEAM5

## Backend Repo has been deployed via Heroku. You don't have to install the backend in your local!
## http://skcshackathon2022-team5.herokuapp.com/
## Or you can install backend in your local computer

## Installation

- Please follow the instructions below if you installed back-end repo for the first time.

## Without Docker
### For Windows

```bash
# Create the env
py -3 -m venv venv

# Activate the env
venv\Scripts\activate

# install packages
pip install -r requirements.txt
```

### For Mac

```bash
# Create the env
python3 -m venv venv

# Activate the env
. venv/bin/activate

# install packages
pip3 install -r requirements.txt
```

## Server start

```bash
# Starts backend server in local
python server.py

# OR

python3 server.py

# Either one of the command should work for you.
# Please DM me if it does not work for you.
```

## With Docker

- Please install Docker desktop app first
- Then you can execute the commands below to setup the backend server using docker image

```bash
# create docker image and name it as podo_back (commands are specified in Dockerfile)
docker build -t sksc-team5 .

# delete all the exisitng containers
docker rm `docker ps -a -q`

# Server start docker container run (http://localhost:5001 for local use) 
docker run -d --name podo_back_container -p 5001:8888 -t sksc-team5

# docker container stop
docker stop sksc-team5-container
```

## For your information

- We are using Fast API Framework for our back-end
- you can check and test all the available apis at http://localhost:5001/docs
- Please pull backend repo daily as I will frequently update the codes.
- Please DO NOT CHANGE ANY CODE and PUSH TO THE MASTER without my permission.
