from flask import Flask , redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return '<h2>Home</h2>'

@app.route('/user/<name>')
def user(name):
  if name == 'admin':
    return redirect(url_for("admin"))
  return f'<h2>{name}</h2>'

@app.route('/admin')
def admin():
  return f'<h2>admin</h2>'

@app.route('/blog/<int:blog_id>')
def blog(blog_id):
  return f'<h2>{blog_id}</h2>'

if __name__ == '__main__':
    app.run(debug=True)
