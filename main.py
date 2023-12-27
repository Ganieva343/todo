from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(100), nullable=False)
   description = db.Column(db.Text, nullable=False)
   status = db.Column(db.Boolean, default=False)


with app.app_context():
   db.create_all()


@app.route('/', methods=['GET'])
def get_todos():
   tasks = db.session.query(Todo).all()
   return render_template("base.html", tasks=tasks, title='Главная страница')


@app.route('/add', methods=['POST'])
def add():
   title = request.form.get('title')
   description = request.form.get('description')
   new_todo = Todo(title=title, description=description, status=False)
   db.session.add(new_todo)
   db.session.commit()
   return redirect(url_for('get_todos'))


@app.route('/view/<int:todo_id>', methods=['GET'])
def view(todo_id):
   todo = Todo.query.filter_by(id=todo_id).first()
   return render_template('view_task.html', todo=todo, title='Просмотр задач')


@app.route('/add_task', methods=['GET'])
def add_task():
   return render_template('add_task.html', title='Новая задача')


@app.route('/update/<int:todo_id>', methods=['GET', 'POST'])
def update(todo_id):
  todo = Todo.query.filter_by(id=todo_id).first()
  if request.method == 'POST':
      todo.title = request.form.get('title')
      todo.description = request.form.get('description')
      db.session.commit()
      return redirect(url_for('get_todos'))
  return render_template('edit_task.html', todo=todo, title='Редактировать')



@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete(todo_id):
   todo = Todo.query.filter_by(id=todo_id).first()
   db.session.delete(todo)
   db.session.commit()
   return redirect(url_for('get_todos'))


if __name__ == "__main__":
    app.run()

