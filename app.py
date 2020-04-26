from flask import Flask, redirect, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import os, datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id_          = db.Column(db.Integer, primary_key=True)
    content      = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return "Task id:<%r>" % self.id_

if not os.path.exists('test.db'):
    db.create_all()
    db.session.commit()

@app.route('/home', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def home():
    """home view"""
    if request.method == 'POST':
        content = request.form['content']
        if content != '':
            db.session.add(Todo(content=content))
            db.session.commit()
            return redirect('/')
        else:
            return render_template('error.html', error='Adding task failed')
    else:
        return render_template('home.html', tasks=Todo.query.all())

@app.route('/delete/<int:id_>')
def delete(id_):
    """delete functionality"""
    task = Todo.query.get_or_404(id_)
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for('home'))
    except:
        return render_template('error.html', error='Deleting task failed')

@app.route('/update/<int:id_>', methods=['GET', 'POST'])
def update(id_):
    """update view"""
    task = Todo.query.get_or_404(id_)
    if request.method == 'POST':
        task.content = request.form['content']
        if task.content != '':
            db.session.commit()
            return redirect(url_for('home'))
        else:
            return render_template('error.html', error='Updating task failed')
    else:
        return render_template('update.html', task=task)

if __name__ == '__main__':
    app.run(debug=True)
