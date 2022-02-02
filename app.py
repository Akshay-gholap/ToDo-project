
from flask import Flask, redirect, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return '<task %r>' % self.id


@app.route('/', methods=['GET','POST'])
def index():
    if request.method=='POST':
        task_content = request.form['content']
        newTask = Todo(content=task_content)

        try:
            db.session.add(newTask)
            db.session.commit()
            return redirect('/')
        except:
            return 'there has been essue adding yourTask'
    else :
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    TaskToDelete= Todo.query.get_or_404(id)

    try:
        db.session.delete(TaskToDelete)
        db.session.commit()
        return redirect('/')
    except:
        return "there was a problem deleting that Task"

@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "there was a problem updating"

    else:
        return render_template('update.html', task=task)


if __name__=="__main__":
    app.run(debug=True)