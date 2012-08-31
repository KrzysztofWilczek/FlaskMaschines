from flask import Flask
from flask import render_template, request, session, redirect, url_for, escape
app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error404.html'), 404

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/')
def index():
    tasks = {}
    machines = {}
    return render_template('index.html', tasks=tasks, machines=machines)

if __name__ == '__main__':
    app.debug = True
    app.run()