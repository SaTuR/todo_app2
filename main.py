from flask import Flask, render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key = True)
    title =db.Column(db.String(100))
    state = db.Column(db.Boolean)


with app.app_context():
    db.create_all()



@app.route("/")
def home():
    lista_tareas = Todo.query.all()
    return render_template("home.html",tareas=lista_tareas)



@app.route("/add", methods=['POST'])
def add():
    title = request.form.get('title')
    new_todo = Todo(title=title, state=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('home'))  



@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.state = not todo.state
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/about")
def about():
    return render_template("about.html")


if __name__== "__main__":
    app.run(debug=True,)