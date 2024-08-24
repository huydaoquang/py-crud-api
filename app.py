from flask import Flask , redirect, url_for, render_template, request,session 
from datetime import timedelta

app = Flask(__name__)

# config session
app.config["SECRET_KEY"] = "huydq"

# config time logout
app.permanent_session_lifetime = timedelta(minutes=1)

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
      return redirect(url_for("user", name=user_name))

  # user is login 
  if "user" in session: 
    return redirect(url_for("user"))
  
  # user is not logged in
  return render_template("login.html")

@app.route("/logout")
def logout():
  session.pop("user", None)
  return redirect(url_for("loginPage"))

@app.route('/user/')
def user():
  if "user" in session: 
    name = session["user"]
    return f'<h2>{name}</h2>'
    if name == 'admin':
      return redirect(url_for("admin"))
  else: 
    return redirect(url_for("loginPage"))
  

@app.route('/admin')
def admin():
  return f'<h2>admin</h2>'

@app.route('/blog/<int:blog_id>')
def blog(blog_id):
  return f'<h2>{blog_id}</h2>'

if __name__ == '__main__':
    app.run(debug=True)
