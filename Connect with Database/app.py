from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Neon database connection
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define Employee model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_of_joining = db.Column(db.Date, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=False)

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    employees = Employee.query.all()
    return render_template('index.html', employees=employees)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        date_of_joining = request.form['date_of_joining']
        department = request.form['department']
        salary = float(request.form['salary'])

        new_emp = Employee(
            name=name,
            date_of_joining=date_of_joining,
            department=department,
            salary=salary
        )
        db.session.add(new_emp)
        db.session.commit()
        return redirect('/')
    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)
