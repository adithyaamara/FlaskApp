from flask import Flask,request,redirect,render_template,Blueprint,session,url_for

admin = Blueprint("admin",__name__,static_folder="static", template_folder="templates")

@admin.route('/',methods = ['GET'])
def default():
    """Default route, redirects to API HOME"""
    if session:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('admin.login'))

#Admin Login and validation#
@admin.route('/login')
def login():
    """Login Screen"""
    if session:
        return redirect(url_for('home'))
    else:
        return render_template('login.html')

#Admin Logout function...
@admin.route('/logout')
def logout():
    if session is None:
        return redirect(url_for('admin.login'))
    session.clear()
    return redirect(url_for('admin.login'))