# William Tom
# 4/13/21

from flask import Flask, render_template, redirect, url_for
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/<name>")
def user (name):
    return f"Hello {name}!"

@app.route("/admin")
def admin():
    return redirect(url_for("/"))

if __name__ == "__main__":
    app.run()

