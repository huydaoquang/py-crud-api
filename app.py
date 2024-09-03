from flask import Flask , redirect, url_for, render_template, request,session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from os import path

app = Flask(__name__)

# config session
app.config["SECRET_KEY"] = "huydq"

# config db
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# config time logout
app.permanent_session_lifetime = timedelta(minutes=1)

db = SQLAlchemy(app)

class User(db.Model):
  user_id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  email = db.Column(db.String(100))

  def __init__(self, name, email):
    self.name = name
    self.email = email

@app.route('/')
def home():
    return render_template("index.html", content = "test" , cars=["bmw", "audi", "toyota"])

@app.route('/home')
def homePage():
    return render_template("home.html")

@app.route('/blog')
def blogPage():
    return render_template("blog.html")

@app.route('/login', methods = ["POST", "GET"])
def loginPage():
  if request.method == "POST": 
    # set time logout
    session.permanent = True
    user_name = request.form["email"]
    password = request.form["password"]
    print("user_name::::", user_name)
    print("password::::", password)
    
    if user_name and password:
      session["user"] = user_name
      found_user = User.query.filter_by(name=user_name).first()
      if found_user:
        session["email"] = found_user.email
      else:
        user = User(user_name, "test@gmail.com")
        db.session.add(user)
        db.session.commit()
        flash("created user in db","info")
      return redirect(url_for("user", name=user_name))

  # user is login 
  if "user" in session: 
    return redirect(url_for("user"))
  
  # user is not logged in
  return render_template("login.html")

@app.route("/logout")
def logout():
  session.pop("user", None)
  flash("user logout ","info")
  return redirect(url_for("loginPage"))

@app.route('/user/', methods=['GET', 'POST'])
def user():
  email = None
  if "user" in session: 
    name = session["user"]
    if request.method == "POST":
      if not request.form["email"] and request.form["name"]:
        User.query.filter_by(name=name).delete()
        db.session.commit()
        flash("Deleted user successfully")
        return redirect(url_for("logout"))
      else:
        email = request.form["email"]
        print("email::::", email)
        session["email"] = email
        found_user = User.query.filter_by(name=name).first()
        found_user.email = email
        db.session.commit()
        flash("email updated!")
    elif "email" in session:
      email = session["email"]
    return render_template("user.html", name=name, email=email)
    if name == 'admin':
      return redirect(url_for("admin"))
  else: 
    flash("You haven't logged in!","info")
    return redirect(url_for("loginPage"))
  

@app.route('/admin')
def admin():
  return f'<h2>admin</h2>'

@app.route('/blog/<int:blog_id>')
def blog(blog_id):
  return f'<h2>{blog_id}</h2>'

if __name__ == '__main__':
  if not path.exists("user.db"):
    with app.app_context():
      db.create_all()
    print("created db success", )
    app.run(debug=True)
