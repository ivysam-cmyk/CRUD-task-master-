from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# to indicate where the database is located. 3 '/' is relative path, exact path is not needed.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# initialize database
db = SQLAlchemy(app)

# id there is already table here, why does there have to be table created in html?(The table here is a model for how the data is added to the table format on html) 
class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  # only content can be controlled by user
  content = db.Column(db.String(200), nullable=False)
  date_created = db.Column(db.DateTime, default = datetime.utcnow)

  # every time a new element is made the repr function will return the task and the id of the task
  def __repr__(self):
    return '<Task %r>' % self.id


@app.route('/', methods = ['POST', 'GET'])
def index():
  if request.method == 'POST':
    # if there is a post method(When you click the submit button, it will post as stated in html) then whatever written in the content will go to this variable
    # task_content is an arbitrary variable
    task_content = request.form['content']
    # pass the string value of the task_content inside the Todo class
    new_task = Todo(content=task_content)

    #if an error is shown in the try part, the except part will return
    try:
      db.session.add(new_task)
      db.session.commit()
      #go back to the home page,wasn't it already on the home page?()
      return redirect('/')
    except:
      return "There was an error adding your task"
  
  else:
    #organise the data by date created
    tasks = Todo.query.order_by(Todo.date_created).all()
    #pass the task data into the template
    return render_template('index.html', tasks=tasks)
  
@app.route('/delete/<int:id>')
def delete(id):
  # store in an arbitrary val, using the unique id inside of  Todo objects, the element 
  task_to_delete = Todo.query.get_or_404(id)

  try:
    #delete the element inside the session and save those changes using commit
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')
  except:
    return "There was a problem deleting that task"


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
  task = Todo.query.get_or_404(id)

  if (request.method == 'POST'):
    task.content = request.form['content']
    try:
      db.session.commit()
      return redirect('/')
    except:
      return 'There was an issue updating your task.'
  else:
    return render_template('update.html', task=task)


if __name__ == "__main__":
  app.run(debug=True)
