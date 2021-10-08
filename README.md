# FlaskApp
A Python - Flask application to demonstrate possible functionalities of Flask Framework 

# Configuration:
```json
{
    "MYSQL_HOST" : "sql6.freesqldatabase.com",
    "MYSQL_USER" : "sqlabcd123",
    "MYSQL_PASSWORD" : "your_password",
    "MYSQL_DB" : "sqldbname",
    "APP_SECRET" : "XXXXXXXXXXXXXX",
    "RandomPassLength" : 10,
    "App_Interface" : "127.0.0.1",
    "MAIL_PASSWORD" : "xxxxxxx",
    "MAIL_SERVER" : "smtp.gmail.com",
    "MAIL_PORT" : 465,
    "MAIL_USERNAME" : "xxxxxxxxxx@gmail.com"
}
```
*MYSQL_XXXXX* : DATABASE related config.
*APP_SECRET* : Used to hash the browser session cookies to avoid cookie tampering attack.
*RandomPassLength* : Once a developer is verified, will get a randomly generated password of length specified here 
*MAIL_XXXX* : Relavant email server config for sending mails to developers using Flask_MySQLdb package. 

# My SQL DB setup:
- If a mysql db  with above configuration is up, Proceed as follows:
- `FlaskApp.sql` has all the required SQL statements for creating and adding sample data to tables [Edit the data insert statements as needed]. Use any helper like `phpmyadmin.co` to execute all the sql statements and setup the database.
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

 # Useful References :
  - Deploy App to production : `https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04` 