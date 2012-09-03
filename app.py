import sqlite3
from flask import Flask, jsonify
from flask import render_template, request, session, g, abort, redirect, url_for, escape
from contextlib import closing
import time, random
from datetime import datetime, timedelta

# App configration part
DATABASE = 'database.db'
SECRET_KEY = '11582925c2f946e0640897f061c76c11f9f52895'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error404.html'), 404

@app.route('/add', methods=['POST'])
def add():
    
    # Check current tasks list
    current_tasks = g.db.execute('select count() as current_tasks from task_maschines tm where stage != 3')
    task_count = current_tasks.fetchone()
    # You can't add new task, maschines still working on previous one
    if (task_count[0] > 0):
        return jsonify(status=False)
    
    # Clear task maschines list
    g.db.execute('delete from task_maschines')
    g.db.commit()
    
    task = request.form['task']
    # Add task and machines to DB
    for machine in request.form.getlist('maschines'):
        now = datetime.now()
        end_time = now+timedelta(seconds=random.randint(1, 60))
        g.db.execute('insert into task_maschines (maschine_id, task_id, stage, end_time) values ('+machine+', '+task+', 1, \''+end_time.strftime('%Y-%m-%d %H:%M:%S')+'\')')
        g.db.commit()
        
    tasks = g.db.execute('select * from task_machines')
    print tasks
    return jsonify(status=True,)

@app.route('/status')
def status():
    
    # Get all current task from DB 
    tasks = g.db.execute('select tm.*, m.name as maschine_name, t.name as task_name from task_maschines tm left join maschines m on m.id = tm.maschine_id left join tasks t on t.id = tm.task_id')
    now = datetime.now()
    task_list = dict()
    for task in tasks.fetchall():
        print task
        # Check end time of current stages for every one task
        end_time = datetime.strptime(task[4], '%Y-%m-%d %H:%M:%S')
        
        stage = task[3]
        next_stage_end_time = task[4]
        
        if (now > end_time):
            if stage == 1:
                stage = 2
            elif stage == 2:
                stage = 3
        
            new_end_time = now+timedelta(seconds=random.randint(1, 60))
            next_stage_end_time = new_end_time.strftime('%Y-%m-%d %H:%M:%S')
            g.db.execute('update task_maschines set stage = '+str(stage)+', end_time = \''+next_stage_end_time+'\' where id = '+str(task[0]))
            g.db.commit()        
        
        # Return list of current tasks and it's stages    
        task_list[task[0]] = dict(maschine_id=task[1],task_id=task[2],stage =stage,maschine_name=task[5],task_name=task[6])
        
    return jsonify(task_list)

# Show some static about page
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/')
def index():

    tasks = g.db.execute('select * from tasks order by id')
    tasks_list = [dict(id=row[0], name=row[1]) for row in tasks.fetchall()]
    
    maschines = g.db.execute('select * from maschines order by id')
    maschines_list = [dict(id=row[0], ip=row[1], name=row[2]) for row in maschines.fetchall()]
    
    return render_template('index.html', tasks = tasks_list, maschines=maschines_list)

if __name__ == '__main__':
    app.run()
    init_db()