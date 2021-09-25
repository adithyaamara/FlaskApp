from flask import Flask,render_template,jsonify,url_for,redirect,request
from flask_mysqldb import MySQL
import json
import time
'''

import MySQLdb.cursors
import re



'''
#Read MySql Config from json
config = json.load(open("config.json",'r'))
#Craete an object of Flak class
app = Flask(__name__)

#print(config)
#Initiate MySql Connection from flask app

app.config['MYSQL_HOST'] = config['MYSQL_HOST']
app.config['MYSQL_USER'] = config['MYSQL_USER']
app.config['MYSQL_PASSWORD'] = config['MYSQL_PASSWORD']
app.config['MYSQL_DB'] = config['MYSQL_DB']
print(config)
mysql = MySQL(app)
#Creating a connection cursor
#cursor = mysql.connection.cursor()
#Executing SQL Statements
#cursor.execute('select * from test')
#data = cursor.fetchone()
#print(data)
#Closing the cursor
#cursor.close()
#Routers
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

@app.route('/')
def admin():
    """Default route, redirects to site-map"""
    #cursor = mysql.connection.cursor()
    #cursor.execute("SELECT 'KILL' + CAST(session_id AS VARCHAR(10)) FROM sys.dm_exec_sessions WHERE is_user_process = 1 AND database_id = DB_ID('sql6439896')")
    #time.sleep(2)
    #cursor.execute("select * from developers")
    #Saving the Actions performed on the DB 
    #mysql.connection.commit()
    
    #print(cursor.fetchone())
    #cursor.close()
    return redirect(url_for('default'))

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
        print(newdev)
        try:
            cursor = mysql.connection.cursor()
            query = "INSERT INTO developers values(\""+ newdev["dev_name"] + "\",\"" + newdev["dev_email"] + "\"," + str(newdev["dev_phone"]) + ",\"" + newdev["dev_city"] + "\"," +str(newdev["dev_age"])+ ")"
            print(query)
            cursor.execute(query)
            cursor.close()
            return render_template('reg_status.html',status="Successful",details=newdev)
        except Exception as e:
            print("/deveregisterdb -> ",e)
            return render_template('reg_status.html',status="Fail")

@app.route('/api')
def default():
    return "<h2 align=\"center\">Flask App V1.0</h2><br><a href='/api/help'>Click Here for Help</a>"

@app.route('/validate', methods = ['POST','GET'])
def validate():
    """Validates Login Received from Login Screen"""
    if request.method == 'POST':
        user = request.form['nm']
        ph = request.form['ph']
        return redirect(url_for('success',name=user,phone=ph))
    if request.method == 'GET':
        user = request.args.get('nm')
        return redirect(url_for('fail'))
    else:
        return redirect(url_for('fail'))
@app.route('/login')
def login():
    """Login Screen"""
    return render_template('login.html')

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
    return render_template('gcharts.html')
if __name__ == '__main__':
    app.run('127.0.0.1',4444,True)
