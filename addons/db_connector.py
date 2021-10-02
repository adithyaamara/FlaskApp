
class db_conn:
    def __init__(self,app:object,config:dict):
        self.app = app
        self.config = config  
    def create_connection(self):
        #Initiate MySql Connection for flask app object
        self.app.config['MYSQL_HOST'] = self.config['MYSQL_HOST']
        self.app.config['MYSQL_USER'] = self.config['MYSQL_USER']
        self.app.config['MYSQL_PASSWORD'] = self.config['MYSQL_PASSWORD']
        self.app.config['MYSQL_DB'] = self.config['MYSQL_DB']
        return self.app