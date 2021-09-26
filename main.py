from flask import Flask,render_template,jsonify,url_for,redirect,request
from flask_mysqldb import MySQL
import json
import time

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
mysql = MySQL(app)

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
    return redirect(url_for('home'))
@app.route('/api',methods = ['GET'])
def home():
    return "<h2 align=\"center\">Flask App V1.0 - Home Page to be built</h2><br><a href='/api/help'>Click Here for Help</a>"

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
            cursor = mysql.connection.cursor()
            query = "select * from developers WHERE PHONE=\""+str(newdev["dev_phone"])+"\" LIMIT 1"
            #print(query)
            cursor.execute(query)
            if cursor.fetchone() is not None:
                cursor.close()
                return render_template('reg_status.html',status="duplicate")
            else:
                query = "INSERT INTO developers values(\""+ str(newdev["dev_name"]) + "\",\"" + str(newdev["dev_email"]) + "\",\"" + str(newdev["dev_phone"]) + "\",\"" + str(newdev["dev_city"]) + "\"," + (newdev["dev_age"])+ ")"
                #print(query)
                cursor.execute(query)
                time.sleep(2)
                mysql.connection.commit()
                cursor.close()
                return render_template('reg_status.html',status="Successful",details=newdev)
        except Exception as e:
            print("/deveregisterdb -> ",e)
            return render_template('reg_status.html',status="Fail")
#Admin Login and validation#
@app.route('/login')
def login():
    """Login Screen"""
    return render_template('login.html')

@app.route('/validate', methods = ['POST'])
def validate():
    """Validates Login Received from Login Screen"""
    if request.method == 'POST':
        id = request.form['id']
        pwd = request.form['pwd']
        query = "SELECT * FROM admins WHERE phone=\"" + str(id) + "\" and pwd=\"" + str(pwd) + "\" LIMIT 1"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        if cursor.fetchone() is not None:   
            cursor.close()
            return f"Login Succesful [Need to redirect to admin dashboard]! Welcome Admin ID- {id}"
        else:
            return "<h2>Unauthorized Access!! <a href='/login'>Try Aagain</a></h2>"

@app.route('/api/help', methods = ['GET'])
def help():
    """Print available functions."""
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return render_template('site-map.html', result = func_list)

@app.route('/charts',methods=['POST','GET'])
def charts():
    """Demo of google charts on static data"""
    if request.method == 'POST':
        return render_template('gcharts.html')
    else:
        return redirect(url_for('login'))
if __name__ == '__main__':
    app.run('127.0.0.1',4444,True)
