
class email_conn:
    def __init__(self,app:object,config:dict):
        self.app = app
        self.config = config 
    def create_connection(self):
        self.app.config['MAIL_SERVER']=self.config["MAIL_SERVER"]
        self.app.config['MAIL_PORT'] = self.config["MAIL_PORT"]
        self.app.config['MAIL_USERNAME'] = self.config["MAIL_USERNAME"]
        self.app.config['MAIL_PASSWORD'] = self.config["MAIL_PASSWORD"]
        self.app.config['MAIL_USE_TLS'] = False
        self.app.config['MAIL_USE_SSL'] = True
        return self.app
