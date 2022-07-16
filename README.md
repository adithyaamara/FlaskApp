# FlaskApp
**A Python - Flask based web application with following features:**

# Contents : 
1. [Features](#features)
2. [Software Stack Used](#software-stack)
3. [Initial Configuration of APP](#initial-configuration)
4. [Deploy With Docker Compose](#deploy_with_docker_compose---easiest-way)
5. [Deploy using Docker, Standalone SQL DB](#usage---docker)
6. [Run Locally For Debugging](#usage---localmachine)
7. [Useful References](#useful-references)

# Features:

1. Any Guest user can register for portal access using a form.
2. Admin users can login to portal --> Approve / Reject access requests received + See details of all registered users.
3. Once Approved, registered person will get credentials via registered email. 
4. Already registered users can request for credentials which will be delivered via registered email.
> **All credentials are by design, hashed and stored in database for enhanced security.**

# Software Stack:

1. My SQL database
2. Python Flask -Web Application
3. PHP MyAdmin [For easier management of sql database]

# Initial Configuration:
> **Please edit this properly before deployment, for app to work properly.**
> The default values in `config.json` are set to match with config we have in docker-compose. 
> Please ensure to do the matching changes in `config.json`, `docker-compose.yml`
```json
{
    "MYSQL_HOST" : "host name / ip of sql database",
    "MYSQL_USER" : "username to login to sql db",
    "MYSQL_PASSWORD" : "password to login to sql db",
    "MYSQL_DB" : "Target database name inside sql db",
    "APP_SECRET" : "XXXXXXXXXXXXXX",
    "RandomPassLength" : 10,
    "App_Interface" : "127.0.0.1 | 0.0.0.0",
    "MAIL_PASSWORD" : "xxxxxxx",
    "MAIL_SERVER" : "smtp.gmail.com",
    "MAIL_PORT" : 465,
    "MAIL_USERNAME" : "xxxxxxxxxx@gmail.com"
}
```
- *MYSQL_XXXXX* : DATABASE related config.
- *APP_SECRET* : Used to hash the browser session cookies to avoid cookie tampering attack. Also same is used for Bcrypt Hashing the passwords stored in SQL DB.
- *RandomPassLength* : Once a developer is verified, will get a randomly generated password of length specified here 
- *MAIL_XXXX* : Relavant email server config for sending mails to developers using Flask_MySQLdb package. 

# Deploy_With_Docker_Compose : 👉 [Easiest Way]
 - Clone the repo using command --> `git clone https://github.com/adithyaamara/FlaskApp.git`
 - Change Current Working Directory to app using cmd --> `cd FlaskApp/`
 - Edit all configurable parameters of this application in `config.json` (Otherwise defaults are applied).
 - Also accordingly edit environment variables of services in `docker-compose.yml` for proper wire up,
    integration between 3 services(php my admin, mysql, python-flask app).
 - Run whole application using `docker-compose up -d --build`
 - First Visit the url --> `http://docker-host-ip:8080` to use PhpMyAdmin and import `FlaskApp.sql` using the UI.
   This should setup all the required back-end databases and tables at once.
   > Doing the above step will by default add a single default admin user to admin database to enable first time login. 
 - Same can be used for any further Databse related operations like adding / deleting admins etc... 
   > It is Recommended to delete the default admin user, add your own admin user by inserting a record to `admins` table using `PHPMyAdmin`. 
   > While adding the admins manually, passwords must be hashed and stored in database. [Hash Your password here](https://bcrypt-generator.com/)
 - Visit the Flask application homepage at `http://docker-host-ip:[4444 | PORT YOU exposed IN docker-compose.yml]` and login with default userid(`1234567890`) and password (`admin`) OR using your own admin credentials if you have added any in previosu step.

# My SQL DB setup:
- If a mysql db  with above configuration specified in `config.json` is up and ready, Proceed as follows:
- `FlaskApp.sql` has all the required SQL statements for creating and adding sample data to tables [Edit the data insert statements if needed]. Use any helper like `phpmyadmin.co` to execute all the sql statements and setup the database.
- Once database is ready with above config, one can proceed to run the application.

# Usage - Docker
 - `git clone https://github.com/adithyaamara/FlaskApp.git`
 -  create a file named `config.json` as templated [above](#Configuration) 
 - `sudo docker build -t flaskapp:v1.0 .`
 - `sudo docker run -d -p4444:4444 flaskapp:v1.0`
 - View HomePage / Site Map At : `http://docker-machine-ip:4444/`

# Usage - LocalMachine
 - `pip install virtualenv`
 - `virtualenv venv`
 - open command prompt and `cd venv`
 - `./Scripts/activate`(For Windows) | `source venv/bin/activate`(For Linux/mac)
 - `git clone https://github.com/adithyaamara/FlaskApp.git`
 - `cd FlaskApp`
 -  create and edit a file named `config.json` as templated [above](#Configuration)
 - `python main.py`
 - view homepage at http://127.0.0.1:4444/

 # Useful References:
  - Deploy App to production : `https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04` 
