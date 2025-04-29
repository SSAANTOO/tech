from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user
from werkzeug.security import generate_password_hash, check_password_hash
import re, datetime
username = ''
address = ''


#from "https://www.geeksforgeeks.org/how-to-add-authentication-to-your-app-with-flask-login/?ref=lbp"
#used some code from "https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application"
app = Flask(__name__)

# basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///Database.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secretkey"

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
#end

#user model
#User data table
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(19), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(20), nullable=False)

#The information's columns

def __init__(self, name, pasw, addr,emai):
   self.username = name
   self.password = pasw
   self.email = emai
   self.address = addr

#Installation data table
class Installation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unid = db.Column(db.Integer, unique=True)
    month = db.Column(db.String(19), nullable=False)
    day = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(19), unique=True, nullable=False)
    address = db.Column(db.String(20), nullable=False)
    installation = db.Column(db.Boolean, nullable=False)
    year = db.Column(db.Integer, nullable=False)

#Consulting data table
class Consulting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unid = db.Column(db.Integer, unique=True)
    month = db.Column(db.String(19), nullable=False)
    day = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(19), unique=True, nullable=False)
    address = db.Column(db.String(20), nullable=False)
    installation = db.Column(db.Boolean, nullable=False)
    year = db.Column(db.Integer, nullable=False)

#create database
with app.app_context():
    db.create_all()


#load users
@login_manager.user_loader
def load_user(username):
    return User.query.get(int(username))


#information page
@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")

#more info page
@app.route("/info", methods=['GET'])
def info():
    return render_template("info.html")

#login page
@app.route("/login", methods=['GET','POST'])
#Login verifies the input data
def login():
    #To be accessed later
    global username
    if request.method == 'POST':

        username = request.form.get("name")
        password = request.form.get("pasw")

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return render_template("hub.html"), username
        else:
            return render_template("login.html", error="Invalid username or password")



    return render_template("login.html")

#registration page
@app.route("/register", methods=['GET','POST'])
def register():
    error = None
    if request.method == "POST" and 'name' in request.form and 'pasw' in request.form and 'addr' in request.form and 'emai' in request.form and 'usercp' in request.form:

        username = request.form.get("name")
        password = request.form.get("pasw")
        address = request.form.get("addr")
        email = request.form.get("emai")
        confirm = request.form.get("usercp")

        #validation checking

        # username unique check
        if not username or not password or not email or not address:
            return render_template("register.html", error='Please fill out the form!')
        elif User.query.filter_by(username=username).first():
            return render_template("register.html", error="Username already taken!")
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            return render_template("register.html", error = 'Invalid email address!')
        elif not re.match(r'[A-Za-z0-9]+', username):
            return render_template("register.html", error = 'Username must contain only letters and numbers!')

        if confirm != password:
            return render_template("register.html", error='Please give the same password.')

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

#new user information added to database
        new_user = User(username=username, password=hashed_password, address=address, email=email)
        db.session.add(new_user)
        db.session.commit()

        return render_template("login.html")
    return render_template("register.html")

@app.route("/consulting", methods=["GET","POST"])
def consulting():
    # global variable of the username is retrieved
    global username, address
    if request.method == "POST" and "date" in request.form:

        # requesting the input data and turned into strings
        date = str(request.form.get("date"))
        # if nothing is entered
        if date == ['']:
            return render_template("con-bok.html", error="please give a date")
        print(date)
        # turn the input data into a list
        date = date.split('-')
        print(date)
        # month
        month = date[1]
        print(month)
        # day
        day = date[2]
        print(day)
        year = date[0]
        """ x = list(datetime.datetime.now())
            d = x[0]
            m= x[1]
            y= x[2]
            if d <= day:
            if m <= month:
                if y <= year:
                    return render_template("con-bok.html", error="please select a date after today")"""
        # creating a unique id using month and days
        if month == '01':
            id = int(day) * int(month) + 11 + int(year)
            print(id)
            month = "january"

        if month == '02':
            id = int(day) * int(month) + 22 + int(year)
            print(id)
            month = "february"

        if month == '03':
            id = int(day) * int(month) + 33 + int(year)
            print(id)
            month = "march"

        if month == '04':
            id = int(day) * int(month) + 44 + int(year)
            print(id)
            month = "april"

        if month == '05':
            id = int(day) * int(month) + 55 + int(year)
            print(id)
            month = "may"

        if month == '06':
            id = int(day) * int(month) + 66 + int(year)
            print(id)
            month = "june"

        if month == '07':
            id = int(day) * int(month) + 77 + int(year)
            print(id)
            month = "july"

        if month == '08':
            id = int(day) * int(month) + 88 + int(year)
            print(id)
            month = "august"

        if month == '09':
            id = int(day) * int(month) + 99 + int(year)
            print(id)
            month = "september"

        if month == '10':
            id = int(day) * int(month) + 1010 + int(year)
            print(id)
            month = "october"

        if month == '11':
            id = int(day) * int(month) + 1111 + int(year)
            print(id)
            month = "november"

        if month == '12':
            id = int(day) * int(month) + 1212 + int(year)
            print(id)
            month = "december"
        print(username)
        year = int(year)
        if address:
            booking = Consulting(unid=id, month=month, day=day, username=username, address=address, installation=True, year=year)
            db.session.add(booking)
            db.session.commit()
        if Consulting.query.filter_by(id=id).first():
            return render_template("con-bok.html", error="date already booked")
        try:
            address = User.query.filter_by(username=username).first().address
        except:
            return render_template("con-bok.html", error="sorry but you already booked")
        print(address)
        try:
            booking = Consulting(unid=id, month=month, day=day, username=username, address=address, installation=True, year=year)
            print(booking)
        except:
            return render_template("con-bok.html", confirm=f'Well done, {date} is now booked!')
        db.session.add(booking)
        db.session.commit()
        return render_template("con-bok.html", confirm=f'Well done, {date} is now booked!'), address

    return render_template("con-bok.html")



meta_data = db.MetaData()

@app.route("/install", methods=["GET","POST"])
def install():
    #global variable of the username is retrieved
    global username, address
    if request.method == "POST" and "date" in request.form:

        #requestning the input data and turned into strings
        date =str(request.form.get("date"))
        #if nothing is entered
        if date ==['']:
            return render_template("inst-bok.html", error="please give a date")
        print(date)
        #turn the input data into a list
        date = date.split('-')
        print(date)
        #month
        month = date[1]
        print(month)
        #day
        day = date[2]
        print(day)
        year = date[0]
        """x = list(datetime.datetime.now())
        d = int(x[0])
        m = int(x[1])
        y = int(x[2])
        if d <= day:
            if m <= month:
                if y <= year:
                    return render_template("con-bok.html", error="please select a date after today")"""
        #creating a unique id using month and days
        if month == '01':
            id = int(day) * int(month)+11+int(year)
            print(id)
            month = "january"

        if month == '02':
            id = int(day) * int(month)+22+int(year)
            print(id)
            month = "february"

        if month == '03':
            id = int(day) * int(month)+33+int(year)
            print(id)
            month = "march"

        if month == '04':
            id = int(day) * int(month)+44+int(year)
            print(id)
            month = "april"

        if month == '05':
            id = int(day) * int(month)+55+int(year)
            print(id)
            month = "may"

        if month == '06':
            id = int(day) * int(month)+66+int(year)
            print(id)
            month = "june"

        if month == '07':
            id = int(day) * int(month)+77+int(year)
            print(id)
            month = "july"

        if month == '08':
            id = int(day) * int(month)+88+int(year)
            print(id)
            month = "august"

        if month == '09':
            id = int(day) * int(month)+99+int(year)
            print(id)
            month = "september"

        if month == '10':
            id = int(day) * int(month)+1010+int(year)
            print(id)
            month = "october"

        if month == '11':
            id = int(day) * int(month)+1111+int(year)
            print(id)
            month = "november"

        if month == '12':
            id = int(day) * int(month)+1212+int(year)
            print(id)
            month = "december"
        print(username)
        year = int(year)
        if address:
            booking = Installation(unid=id, month=month, day=day, username=username, address=address, installation=True, year=year)
            db.session.add(booking)
            db.session.commit()
            return render_template("inst-bok.html", confirm = f'Well done, {date} is now booked!'), address
        if Installation.query.filter_by(id=id).first():
            return render_template("inst-bok.html", error="date already booked")
        try:
            address = User.query.filter_by(username=username).first().address
        except:
            return render_template("inst-bok.html", error= "sorry but you already booked")
        print(address)
        booking = Installation(unid=id, month=month, day=day, username=username, address=address, installation=True)
        print(booking)

        db.session.add(booking)
        db.session.commit()
        return render_template("inst-bok.html", confirm = f'Well done, {date} is now booked!'), address


    return render_template("inst-bok.html")


@app.route("/hub")
def hub():
    return render_template("hub.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/benefits1")
def benefits1():
    return render_template("ben1.html")

@app.route("/benefits")
def benefits():
    return render_template("ben.html")

@app.route("/installation1")
def installation1():
    return render_template("installation1.html")

@app.route("/installation")
def installation():
    return render_template("installation.html")

@app.route("/about1")
def about1():
    return render_template("about1.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/solar1")
def solar1():
    return render_template("solar1.html")

@app.route("/solar")
def solar():
    return render_template("solar.html")


carbon_t = 0
carbon = False
carbon_w = 0
carbon_c = 0
carbon_n = 0
carbon_cd = 0
@app.route("/carbon", methods=["GET","POST"])
def carbon():
    if request.method == "POST" and 'wood' in request.form or 'coal' in request.form or 'natural-gas' in request.form or 'car' in request.form or 'car-time' in request.form:
        global carbon, carbon_t, carbon_cd, carbon_n, carbon_w, carbon_c

        # create the final variables#
        carbon_t = 0
        carbon = False
        carbon_w = 0
        carbon_c = 0
        carbon_n = 0
        carbon_cd = 0

        # get the input data from user
        wood = int(request.form.get("wood"))
        coal = int(request.form.get("coal"))
        natural = int(request.form.get("natural-gas"))
        car_dis = int(request.form.get("car"))
        car_tim = int(request.form.get("car-time"))


            # wood calculation
        if wood > 0: # This will check if it is a valid value (not empty or zero)
            wood = float(wood)
            carbon_w = wood * 0.7
            carbon_w = float(carbon_w)
            carbon = True
            print(carbon_w)

            # coal calculation
        if coal > 0: # This will check if it is a valid value (not empty or zero)
            coal = float(coal)
            carbon_c = coal * 0.8
            carbon_c = float(carbon_c)
            carbon = True
            print(carbon_c)

            # natural gas calculation
        if natural > 0: # This will check if it is a valid value (not empty or zero)
            natural = float(natural)
            carbon_n = natural * 0.5
            carbon_n = float(carbon_n)
            carbon = True
            print(carbon_n)

            # car distance calculation
        if car_dis > 0: # This will check if it is a valid value (not empty or zero)
            car_dis = float(car_dis)
            carbon_cd = car_dis * 165
            carbon_cd = carbon_cd / 100
            carbon_cd = float(carbon_cd)
            carbon = True
            print(carbon_cd)

            # car time calculation
        if car_tim > 0: # This will check if it is a valid value (not empty or zero)
            # car_tim = int(car_tim)
            carbon_t = car_tim * 140
            carbon_t = carbon_t / 100
            carbon_t = float(carbon_t)
            carbon = True
            print(carbon_t)


    return render_template("carbon.html", carbon=carbon, carbon_t=carbon_t, carbon_cd=carbon_cd, carbon_n=carbon_n, carbon_w=carbon_w, carbon_c=carbon_c )



if __name__ == '__main__':

    app.run(debug=True)