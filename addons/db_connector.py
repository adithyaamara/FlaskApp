from flask_mysqldb import MySQL

class db_conn:
    def __init__(self,app:object,config:dict):
        self.app = app
        self._config = config
        self.app.config['MYSQL_HOST'] = self._config['MYSQL_HOST']
        self.app.config['MYSQL_USER'] = self._config['MYSQL_USER']
        self.app.config['MYSQL_PASSWORD'] = self._config['MYSQL_PASSWORD']
        self.app.config['MYSQL_DB'] = self._config['MYSQL_DB']  
        self.mysql = MySQL(self.app)
    def create_connection(self):
        #Initiate MySql Connection for flask app object
        return self.app
    
    def db_transaction(self,query:str,rec_count,commit_req:bool):
        try:
            cursor = self.mysql.connection.cursor()
            print("DB CONNECTION SUCCESSFUL!!!!!!!!")
        except Exception as e:
            print("Mysql Connection error : ",e)
            return "conn_err"
        cursor.execute(query)
        if commit_req == True:
            self.mysql.connection.commit()  #Commiting the sql state and returning null because insert statements don't return any records.
            return None
        if rec_count == 1:
            result = cursor.fetchone()
            cursor.close()
            return result
        else:
            result = cursor.fetchall()
            cursor.close()
            return result
