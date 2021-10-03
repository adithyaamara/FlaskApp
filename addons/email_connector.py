from flask_mail import Mail, Message

class email_conn:
    def __init__(self,app:object,config:dict):
        self.app = app
        self.config = config 
        self.app.config['MAIL_SERVER']=self.config["MAIL_SERVER"]
        self.app.config['MAIL_PORT'] = self.config["MAIL_PORT"]
        self.app.config['MAIL_USERNAME'] = self.config["MAIL_USERNAME"]
        self.app.config['MAIL_PASSWORD'] = self.config["MAIL_PASSWORD"]
        self.app.config['MAIL_USE_TLS'] = False
        self.app.config['MAIL_USE_SSL'] = True
        self._sender_email = config["MAIL_USERNAME"]
        try:
            self.mail = Mail(self.app)
            print("Authentication Successful.......!!")
        except Exception as e:
            print("Email server error : ",e)
    def create_connection(self):
        #Initiate Mail usage for flask app.
        return self.app
    
    def send_mail(self,subject:str,msg_body:str,recipients):
        msg = Message(
                subject,
                sender = self._sender_email,
                recipients = [recipients]
               )
        msg.body = msg_body
        try:
            self.mail.send(msg)
            return "success"
        except Exception as e:
            print("Something Wrong with the SMTP Server!!!!!!!!!!!!! :",e)
            return None