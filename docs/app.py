from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route("/",methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo= Todo.query.all()
    return render_template('index.html',allTodo=allTodo)

@app.route("/show")
def show():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'Showing all todos'

@app.route("/update/<int:sno>",methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo= Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo= Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)

@app.route("/delete/<int:sno>")
def product(sno):
    todo= Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/search", methods=['GET'])
def search():
    query = request.args.get('query')
    results = Todo.query.filter(Todo.title.contains(query) | Todo.desc.contains(query)).all()
    return render_template('search.html', results=results, query=query)
@app.route("/search_by_date", methods=['GET', 'POST'])
def search_by_date():
    if request.method == 'POST':
        search_date_str = request.form['search_date']
        search_date = datetime.strptime(search_date_str, '%Y-%m-%d').date()
        results = Todo.query.filter(db.func.date(Todo.date_created) == search_date).all()
        return render_template('search_by_date.html', results=results, search_date=search_date_str)
    return render_template('search_by_date.html')
if __name__ == "__main__":
    # Create the database and the database table
    with app.app_context():
        db.create_all()

    # Run the Flask application
    app.run(debug=True, port=8000)

