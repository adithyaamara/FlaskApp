from flask_mysqldb import MySQL
import json
import os

path_to_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.json')
config = json.load(open(path_to_json,'r'))

class db_conn:
    def __init__(self,app:object):
        self.app = app
          
    def create_connection(self):
        #Initiate MySql Connection for flask app object
        self.app.config['MYSQL_HOST'] = config['MYSQL_HOST']
        self.app.config['MYSQL_USER'] = config['MYSQL_USER']
        self.app.config['MYSQL_PASSWORD'] = config['MYSQL_PASSWORD']
        self.app.config['MYSQL_DB'] = config['MYSQL_DB']
        return self.app