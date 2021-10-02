from flask_mail import Mail, Message
import json
import os

path_to_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.json')
config = json.load(open(path_to_json,'r'))

class email_conn:
    def __init__(self,app:object):
        self.app = app 
    def create_connection(self):
        self.app.config['MAIL_SERVER']=config["MAIL_SERVER"]
        self.app.config['MAIL_PORT'] = config["MAIL_PORT"]
        self.app.config['MAIL_USERNAME'] = config["MAIL_USERNAME"]
        self.app.config['MAIL_PASSWORD'] = config["MAIL_PASSWORD"]
        self.app.config['MAIL_USE_TLS'] = False
        self.app.config['MAIL_USE_SSL'] = True
        return self.app
