from flask import Flask,render_template,url_for,redirect,request,session
import json
import time
from flask_mail import Mail, Message

from addons.db_connector import db_conn
from addons.email_connector import email_conn
from addons.password_gen import pwd_gen

#Import blueprints for guest and amin routes
from guest.views import view
from admin.views import admin

#Read MySql Config from json
config = json.load(open("config.json",'r'))

#Craete an object of Flak class
app = Flask(__name__)

#Register blueprints
app.register_blueprint(admin)
app.register_blueprint(view)

#Initiate MySql Connection from flask app
db_obj = db_conn(app,config)
app = db_obj.create_connection()

#Flask App secret
app.secret_key = config["APP_SECRET"]

#Email Mechanism Initialization
app = email_conn(app,config).create_connection()
try:
    mail = Mail(app)
    print("Authentication Successful.......!!")
except Exception as e:
    print("Email server error : ",e)

#Routes -- Transferred to admin,guest views&blueprint

@app.route('/api/home',methods = ['GET'])
def home():
    if session:
        try:
            query = "select count(PHONE) from developers"
            acc = db_obj.db_transaction(query,1,False)
            session['pr'] = acc[0] or '0'
            query = "select count(ID) from verified_devs"
            acc = db_obj.db_transaction(query,1,False)
            session['rd'] = acc[0] or '0'
            return render_template('home.html')
        except Exception as e:
            return render_template('home.html')
    else:
         return redirect(url_for('admin.login'))

@app.route('/devregisterdb',methods=['POST'])
def devregisterdb():
    if request.method == 'POST':
        newdev = {}
        newdev["dev_name"] = request.form["name"]
        newdev["dev_email"] = request.form["email"]
        newdev["dev_phone"] = request.form["phone"]
        newdev["dev_city"] = request.form["city"]
        newdev["dev_age"] = request.form["age"]
        #print(newdev)
        try:
            query = "select * from developers WHERE PHONE=\""+str(newdev["dev_phone"])+"\" LIMIT 1"
            res = db_obj.db_transaction(query,1,False)
            if res == "conn_err":
                res = None
                return render_template('Register.html',status="unavailable")
            if res is not None:
                res = None
                return render_template('Register.html',status="dup_ph")
            res = None
            query = "select * from developers WHERE EMAIL=\""+str(newdev["dev_email"])+"\" LIMIT 1"
            res = db_obj.db_transaction(query,1,False)
            if res is not None:
                return render_template('Register.html',status="dup_email")
            else:
                res = None
                query = "INSERT INTO developers values(\""+ str(newdev["dev_name"]) + "\",\"" + str(newdev["dev_email"]) + "\",\"" + str(newdev["dev_phone"]) + "\",\"" + str(newdev["dev_city"]) + "\"," + (newdev["dev_age"])+ ")"
                res = db_obj.db_transaction(query,2,True)
                time.sleep(1)
                return render_template('Register.html',status="Successful",details=newdev)
        except Exception as e:
            print("/deveregisterdb -> ",e)
            return render_template('Register.html',status="Fail")
#---------------------------------------------------------------------------------------------------------------------------------------------------#
@app.route('/validate', methods = ['POST'])
def validate():
    """Validates Login Received from Login Screen"""
    if request.method == 'POST':
        id = request.form['id']
        pwd = request.form['pwd']
        query = "SELECT * FROM admins WHERE phone=\"" + str(id) + "\" and pwd=\"" + str(pwd) + "\" LIMIT 1"
        res = db_obj.db_transaction(query,1,False)
        if res == "conn_err":
            print("DB Error : ",e)
            return render_template('login.html',err = "conn_err")
        if res is not None:   
            session["loggedin"] = True
            session["userid"] = res[2]
            session["name"] = res[1]
            query = "select count(PHONE) from developers"
            acc = db_obj.db_transaction(query,1,False) ##Give 3rd arg is False for all select queries, True for insert queries.
            session['pr'] = acc[0]
            return redirect(url_for('home'))
        else:
            return render_template('login.html',err = "True")
#------------------------------------------------------------------------------------------------------#
#----------Approvals page---------------#
@app.route('/approvals',methods=['GET'])
def approvals():
    if session:
        query = "select * from developers"
        records = db_obj.db_transaction(query,2,False)
        return render_template('approvals.html',records=records)
    else:
        return render_template('login.html')

@app.route('/process_entry/<d>/<id>')
def process(d,id):
    if session:
        if d == "A":
            query = "select * from developers where PHONE=\""+id+"\" LIMIT 1"
            rec = db_obj.db_transaction(query,1,False)  #Commit required is False for all select/Read type statements.
            if rec == "conn_err":
                return "Database Unavailable! Try again sometime later!!"
            randompass = pwd_gen(int(config["RandomPassLength"])).genarate() #Using pwd_gen class' generate method for password generation
            if rec:
                query = "INSERT INTO verified_devs values(\""+ "\",\"" + str(rec[0]) + "\",\"" + str(rec[1]) + "\",\"" + str(rec[2]) + "\",\"" + str(rec[3]) + "\"," + str(rec[4]) +",\""+randompass+"\")"
                res = db_obj.db_transaction(query,0,True) #For commit true given, 2nd arg "record count to return" is ignored because we don't need return records for commit transactions.
                if res == "conn_err":
                    print("DB Error. Transaction Failed")
                    return("",204)
                query = "delete from developers where PHONE=\""+id+"\""
                res = None #Setting res is None to avoid furthur flase positives.
                res = db_obj.db_transaction(query,0,True)
                if res == "conn_err":
                    print("DB Error. Transaction Failed")
                    return("",204)
                else:
                    return("",204)
        if d == "R":
            query = "delete from developers where PHONE=\""+id+"\""
            res = db_obj.db_transaction(query,0,True)
            if res == "conn_err":
                print("DB Error!!")
                return("",204)
            else:
                return("",204)            
    else:
        return(redirect(url_for('login')))
#----------------------------------------#
#------------Registered Developers Viewer-------------------#
@app.route('/get_devs')
def get_devs():
    if session:
        query = "select * from verified_devs"
        rec = db_obj.db_transaction(query,2,False)
        if rec == "conn_err":
            print("DB error!!!")
            return("",204)
        else:
            return render_template("verified_devs.html",rec=rec)
    else:
        return redirect(url_for('login'))
#-----------Service Requests------------------#
@app.route('/devsr',methods=['GET']) #Serves form template for passwordd request
def request_form():
    return render_template('dev_services.html')

@app.route('/devsr/send',methods=['POST','GET'])  #Handles POST request arrived from dev_services.html
def sendmail():
    if request.method=='GET':
        return redirect(url_for('request_form'))
    email = request.form["email"]
    query = "select PWD from verified_devs where EMAIL=\"" + email + "\"LIMIT 1"
    pwd = db_obj.db_transaction(query,1,False)
    if pwd == "conn_err":
        return render_template('dev_services.html',err="db")
    if pwd is None:
        return render_template('dev_services.html',err="unregistered")
    pwd = pwd[0]
    sender_email = config["MAIL_USERNAME"]
    SUBJECT = "Response to your recent service request with flask app!!"
    TEXT = "Your password for the Flask portal is : " + pwd
    msg = Message(
                SUBJECT,
                sender =sender_email,
                recipients = [email]
               )
    msg.body = TEXT
    try:
        mail.send(msg)
        return render_template('dev_services.html',err="Successful")
    except Exception as e:
        print("Something Wrong with the SMTP Server!!!!!!!!!!!!! :" ,e)
        return render_template('dev_services.html',err="db")
#----------------------------------------#
@app.route('/api/help', methods = ['GET'])
def help():
    """Print available functions."""
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return render_template('site-map.html', result = func_list)

if __name__ == '__main__':
    config = json.load(open("config.json",'r'))
    Interface = config["App_Interface"]
    app.run(Interface,4444,True)
