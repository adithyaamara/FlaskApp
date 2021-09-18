# FlaskApp
A Python - Flask application to demonstrate possible functionalities of Flask Framework 

# Usage - Docker
 - `git clone https://github.com/adithyaamara/FlaskApp.git`
 - `sudo docker build -t flaskapp:v1.0 .`
 - `sudo docker run -d -p4444:4444 flaskapp:v1.0`
 - View HomePage / Site Map At : `http://docker-machine-ip:4444/`

#Usage - LocalMachine
 - `pip install virtualenv`
 - `virtualenv venv`
 - open command prompt and `cd venv`
 - `./Scripts/activate`(For Windows) | `source venv/bin/activate`(For Linux/mac)
 - `git clone https://github.com/adithyaamara/FlaskApp.git`
 - `cd FlaskApp`
 - `python main.py`