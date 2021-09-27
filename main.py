from flask import Flask,render_template,url_for,redirect,request,session
from flask_mysqldb import MySQL
import json
import time
import string
import random
#Read MySql Config from json
config = json.load(open("config.json",'r'))
#print(config)

#Craete an object of Flak class
app = Flask(__name__)

#Initiate MySql Connection from flask app
app.config['MYSQL_HOST'] = config['MYSQL_HOST']
app.config['MYSQL_USER'] = config['MYSQL_USER']
app.config['MYSQL_PASSWORD'] = config['MYSQL_PASSWORD']
app.config['MYSQL_DB'] = config['MYSQL_DB']

app.secret_key = config["APP_SECRET"]

mysql = MySQL(app)


#-------password generator-------#
lower = string.ascii_lowercase
upper = string.ascii_uppercase
num = string.digits
all = lower + upper + num
length = config["RandomPassLength"]
#---------------------------------#

#Routes

#------Jinja Templating Example-------------#
@app.route('/result')
def display():
    """Result Grabber with submit and reset"""
    return render_template('result.html')

@app.route('/marks',methods = ['POST','GET'])
def marks():
    """Displays grabbed marks from grabber, with added css"""
    dict = {}
    total = 0
    for k,v in request.form.items():
        dict[k] = v
        total = total + float(v)
    dict["Total"] = total
    if request.method == 'GET':
        return "Get is blocked"
    return render_template('marks.html', result = dict)
#-----------------------------------------------------------#

@app.route('/',methods = ['GET'])
def admin():
    """Default route, redirects to API HOME"""
    if session:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

@app.route('/api/home',methods = ['GET'])
def home():
    if session:
        try:
            cursor = mysql.connection.cursor()
            query = "select count(PHONE) from developers"
            cursor.execute(query)
            acc = cursor.fetchone()
            session['pr'] = acc[0] or '0'
            query = "select count(ID) from verified_devs"
            cursor.execute(query)
            acc = cursor.fetchone()
            session['rd'] = acc[0] or '0'
            cursor.close()
            return render_template('home.html')
        except Exception as e:
            return render_template('home.html')
    else:
         return redirect(url_for('login'))
#------Developer registrations----------------#
@app.route("/dev_register",methods = ['GET'])
def dev_register():
    return render_template('Register.html')

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
            try:
                cursor = mysql.connection.cursor()
            except Exception as e:
                return render_template('Register.html',status="unavailable")
            query = "select * from developers WHERE PHONE=\""+str(newdev["dev_phone"])+"\" LIMIT 1"
            #print(query)
            cursor.execute(query)
            if cursor.fetchone() is not None:
                cursor.close()
                return render_template('Register.html',status="dup_ph")
            query = "select * from developers WHERE EMAIL=\""+str(newdev["dev_email"])+"\" LIMIT 1"
            cursor.execute(query)
            if cursor.fetchone() is not None:
                cursor.close()
                return render_template('Register.html',status="dup_email")
            else:
                query = "INSERT INTO developers values(\""+ str(newdev["dev_name"]) + "\",\"" + str(newdev["dev_email"]) + "\",\"" + str(newdev["dev_phone"]) + "\",\"" + str(newdev["dev_city"]) + "\"," + (newdev["dev_age"])+ ")"
                #print(query)
                cursor.execute(query)
                time.sleep(2)
                mysql.connection.commit()
                cursor.close()
                return render_template('Register.html',status="Successful",details=newdev)
        except Exception as e:
            print("/deveregisterdb -> ",e)
            return render_template('Register.html',status="Fail")
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#Admin Login and validation#
@app.route('/login')
def login():
    """Login Screen"""
    if session:
        return redirect(url_for('home'))
    else:
        return render_template('login.html')

@app.route('/validate', methods = ['POST'])
def validate():
    """Validates Login Received from Login Screen"""
    if request.method == 'POST':
        id = request.form['id']
        pwd = request.form['pwd']
        query = "SELECT * FROM admins WHERE phone=\"" + str(id) + "\" and pwd=\"" + str(pwd) + "\" LIMIT 1"
        try:
            cursor = mysql.connection.cursor()
        except Exception as e:
            print("DB Error : ",e)
            return render_template('login.html',err = "conn_err")
        cursor.execute(query)
        acc = cursor.fetchone()
        if acc is not None:   
            session["loggedin"] = True
            session["userid"] = acc[2]
            session["name"] = acc[1]
            query = "select count(PHONE) from developers"
            cursor.execute(query)
            acc = cursor.fetchone()
            session['pr'] = acc[0]
            cursor.close()
            return redirect(url_for('home'))
        else:
            return render_template('login.html',err = "True")
#------------------------------------------------------------------------------------------------------#
#----------Approvals page---------------#
@app.route('/approvals',methods=['GET'])
def approvals():
    if session:
        cursor = mysql.connection.cursor()
        query = "select * from developers"
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        return render_template('approvals.html',records=records)
    else:
        return redirect(url_for(login))

@app.route('/process_entry/<d>/<id>')
def process(d,id):
    if session:
        if d == "A":
            try:
                cursor = mysql.connection.cursor()
            except Exception as e:
                print("db error : ",e)
                return f"Service Unavailable..rECEIVED TILL R. Id received {id}"
            query = "select * from developers where PHONE=\""+id+"\" LIMIT 1"
            cursor.execute(query)
            rec = cursor.fetchone()
            temp = random.sample(all,length)
            randompass = "".join(temp)
            if rec:
                query = "INSERT INTO verified_devs values(\""+ "\",\"" + str(rec[0]) + "\",\"" + str(rec[1]) + "\",\"" + str(rec[2]) + "\",\"" + str(rec[3]) + "\"," + str(rec[4]) +",\""+randompass+"\")"
                try:
                    cursor.execute(query)
                    query = "delete from developers where PHONE=\""+id+"\""
                    time.sleep(1)
                    cursor.execute(query)
                    mysql.connection.commit()
                    cursor.close()
                except Exception as e:
                    print("DB Error",e)
                return("",204)
        if d == "R":
            try:
                cursor = mysql.connection.cursor()
            except Exception as e:
                print("db error : ",e)
                return f"Service Unavailable..rECEIVED TILL R. Id received {id}"
            query = "delete from developers where PHONE=\""+id+"\""
            cursor.execute(query)
            mysql.connection.commit()
            cursor.close()
            return("",204)
        else:
            return('',204)            
    else:
        return(redirect(url_for('login')))
#----------------------------------------#
#----------------------------------------#
@app.route('/get_devs')
def get_devs():
    if session:
        try:
            cursor = mysql.connection.cursor()
        except Exception as e:
            print("db error : ",e)
        query = "select * from verified_devs"
        cursor.execute(query)
        rec = cursor.fetchall()
        return render_template("verified_devs.html",rec=rec)
    else:
        return redirect(url_for('login'))
#----------------------------------------#
#Admin Logout function...
@app.route('/logout')
def logout():
    if session is None:
        return redirect(url_for('login'))
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/help', methods = ['GET'])
def help():
    """Print available functions."""
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return render_template('site-map.html', result = func_list)

@app.route('/charts',methods=['GET'])
def charts():
    """Demo of google charts on static data"""
    if request.method == 'GET' and session:
        return render_template('gcharts.html')
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run('127.0.0.1',4444,True)
