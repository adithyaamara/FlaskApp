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
    "RandomPassLength" : 10
}
```
*MYSQL_XXXXX* : DATABASE related config.
*APP_SECRET* : Used to hash the browser session cookies to avoid cookie tampering attack.
*RandomPassLength* : Once a developer is verified, will get a randomly generated password of length specified here 

# Requirements:
- A mysql db  with above configuration, following tables.

```
DATABASE_NAME.developer -- For accepting developer registrations from a form.

NAME VARCHAR(50)
EMAIL VARCHAR(50)
PHONE INT
CITY VARCHAR(30)
AGE INT

```

```
DATABASE_NAME.admins -- For holding lsit of site admins and their login credentials :

NAME VARCHAR(50)
EMAIL VARCHAR(50)
PHONE INT
CITY VARCHAR(30)
AGE INT
PWD varchar(30)

```

# Usage - Docker
 - `git clone https://github.com/adithyaamara/FlaskApp.git`
 -  edit main.py's app.run() to replace `127.0.0.1` with `0.0.0.0` to run app on all network interfaces. 
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
 - `python -m main.py`
 - view homepage at http://127.0.0.1:4444/