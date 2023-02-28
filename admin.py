from flask import Flask, render_template, redirect, url_for, request,flash
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin,current_user
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf import FlaskForm

import lockerinfo as l
import talkapi as t

app=Flask(__name__)
app.secret_key="We love Johnstone That is true!!!"

login_manager= LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

USERS=[{"id":1,"name":"LILY","password":generate_password_hash('123')},{"id":2,"name":"lili","password":generate_password_hash('456')}]

def create_user(user_name,password):
    user={"name":user_name,"password":generate_password_hash(password),"id":uuid.uuid4()}
    users.append(user)

def get_user(user_name):
    for user in USERS:
        if user.get('name')==user_name:
            return user

    return None

class User(UserMixin):
    def __init__(self,user):
        self.username=user.get('name')
        self.password_hash=user.get('password')
        self.id=user.get('id')

    def verify_password(self,password):
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash,password)

    def get_id(self):
        return self.id

    @staticmethod
    def get(user_id):
        if not user_id:
            return None
        for user in USERS:
            if user.get('id')==user_id:
                return User(user)
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

class LoginForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired()])
    password=PasswordField("Password", validators=[DataRequired()])


@app.route("/login",methods=['GET','POST'])
def login():
    form=LoginForm()
    emsg=None
    if form.validate_on_submit():
        user_name=form.username.data
        password=form.password.data
        user_info=get_user(user_name)
        if user_info is None:
            emsg="Username or password is invalid"
        else:
            user=User(user_info)
            if user.verify_password(password):
                login_user(user)
                return redirect(request.args.get('next') or url_for("index"))
            else:
                emsg="Username or password is invalid"
    return render_template('login.html',form=form,emsg=emsg)

@app.route("/")
@login_required
def index():
    return render_template('index.html',username=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('index'))

@app.route('/lockers',methods=['GET','POST'])
@login_required
def lockers():
    if request.method=="POST":
        result=request.form.to_dict()
        result=list(result.keys())[0].replace(" ","").split("\n")
        newlocation=result[1]
        newbranch=result[2]
        newavail=result[3]
        newoid=result[4]
        newpasscode=result[5]
        newstagetime=result[6]
        l.edit_locker(newlocation,newavail,newoid,newstagetime)
        flash("Lockers info updated!!!",category="info")

    locker_info=l.lockers()
    return render_template('locker.html',locker_info=locker_info)

@app.route('/deletelockers',methods=['POST'])
@login_required
def deletelockers():
    if request.method=="POST":
        result=request.form.to_dict()
        result=list(result.keys())[0].replace(" ","").split("\n")
        newlocation=result[1]
        newbranch=result[2]
        newavail=result[3]
        newoid=result[4]
        newpasscode=result[5]
        newstagetime=result[6]
        l.delete_locker(newlocation,newbranch)
        flash("Lockers infor updated!!!",category="info")
    return redirect(url_for("lockers"))


@app.route('/add_lockers',methods=['GET','POST'])
@login_required
def add_lockers():
    if request.method=='POST':
        location=request.form['Location']
        branch=request.form['Branch']
        locations=l.check_location()
        if location not in locations:
            if location and branch:
                l.add_locker(branch,location)
                flash("New Location was Added",category="info")
                return redirect(url_for("lockers"))
            else:
                flash("Invaile location or branch", category='warning')
                return render_template('add_lockers.html')
        else:
            flash("This Location already exist, Please rename the location",category='warning')
            return render_template('add_lockers.html')
    else:
        return render_template('add_lockers.html')

@app.route('/client')
@login_required
def client():
    return render_template('client.html')

@app.route('/picking',methods=['GET','POST'])
@login_required
def picking():
    if request.method=="POST":
        password=request.form["password"]
        branch='JAXS160'
        verify=l.verify_locker(password,branch)
        print(verify)
        if verify:
            oid=verify[3]
            if oid:
                oidinfo=t.talkshow(oid)
                return render_template('signiture.html',oidinfo=oidinfo)
            else:
                flash("Sorry, There is something wrong. Please contact store for assist",category="warning")
                return render_template('picking.html')
        else:
            flash("Sorry, No passcode match. Please put the correct Passcode",category="warning")
            return render_template('picking.html')

    else:
        return render_template('picking.html')

@app.route('/signiture',methods=['GET','POST'])
@login_required
def signiture():
    if request.method=="POST":
        l.open_locker(location)
        l.avail_locker(location)
        flash("The door is open, Please pick your order. Thank you.",category="info")
    return render_template('signiture.html')

@app.route('/staging',methods=['GET','POST'])
@login_required
def staging():
    if request.method=="POST":
        result=request.form.to_dict()
        result=list(result.keys())[0].replace(" ","").split("\n")
        newlocation=result[1]
        newbranch=result[2]
        newavail=result[3]
        newoid=result[4]
        newpasscode=result[5]
        newstagetime=result[6]
        l.delete_locker(newlocation,newbranch)
        flash("Lockers infor updated!!!",category="info")
    return redirect(url_for("lockers"))


if __name__=="__main__":
    app.run(debug=True)