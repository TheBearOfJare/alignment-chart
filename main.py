import os
from flask import Flask, render_template

app = Flask(__name__, template_folder='src', static_folder='src')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/view")
def view():
    return render_template('view.html', q1='Q1', q2='Q2', q3='Q3', q4='Q4')

def main():
    app.run(port=int(os.environ.get('PORT', 80)))

if __name__ == "__main__":
    main()
