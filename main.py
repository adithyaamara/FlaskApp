from flask import Flask,render_template,jsonify,url_for,redirect,request
'''
from flask_mysqldb import MySQL
import json
import MySQLdb.cursors
import re
import time

#Read MySql Config from json
config = json.load(open("config.json",'r'))
'''
#Craete an object of Flak class
app = Flask(__name__)

#print(config)
#Initiate MySql Connection from flask app
'''
app.config['MYSQL_HOST'] = config['MYSQL_HOST']
app.config['MYSQL_USER'] = config['MYSQL_USER']
app.config['MYSQL_PASSWORD'] = config['MYSQL_PASSWORD']
app.config['MYSQL_DB'] = config['MYSQL_DB']
#print(config)
mysql = MySQL(app)
''' 
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
    '''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('CREATE TABLE test(ID int,NAME varchar(20),AGE int)')
    time.sleep(2)
    cursor.execute('INSERT INTO test values(1,"Adi",23);INSERT INTO test values(2,"Ram",24)')
    cursor.execute('select * from test')
    data=cursor.fetchone()
    print(data)
    '''
    #Saving the Actions performed on the DB 
    #mysql.connection.commit()
    return redirect(url_for('help'))
@app.route('/api')
def api():
    """Default route, redirects to sitemap"""
    return redirect(url_for('help'))
@app.route('/api')
def default():
    return "<h2 align=\"center\">Flask App V1.0</h2>"
@app.route('/user/<name>')
def user(name):
    if name=='adithya':
        return "Let's redirect you to : " + str(url_for('admin'))
    else:
        return f"Tester Logged in : {name}"
@app.route('/success/<name>&<phone>' ,methods=['POST','GET'])
def success(name,phone):
    """Login Screen post ethod redirects to here"""
    if request.method == 'GET':
        return render_template('success.html',name=name,phone=phone)
    else:
        return "Method Blocked"
@app.route('/fail/<name>')
def fail(name):
    """Login screen get method is blocked and redirected to here"""
    return f"I don't know you! Just stay away from me {name}!!!"

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
    app.run('0.0.0.0',4444,True)
