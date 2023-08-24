set-1

1.)--What is Flask and its benefits?
Flask is an API of Python that allows us to build up web-applications. It was developed by Armin Ronacher.
Flask's framework is more explicit than Django's framework
and is also easier to learn because it has less base code to implement a simple web-Application.

3.)--from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    tablename = 'user'

    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        return True

    def get_id(self):
        return self.email

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False


2.)--from pymongo import MongoClient


class HospitalDB:
    def init(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['Hospital']
        self.doctors = self.db['Doctor']
        self.patients = self.db['Patient']
        self.medicines = self.db['Medicine']

    def create_doctor(self, doctor):
        result = self.doctors.insert_one(doctor)
        return result.inserted_id

    def create_patient(self, patient):
        result = self.patients.insert_one(patient)
        return result.inserted_id

    def create_medicine(self, medicine):
        result = self.medicines.insert_one(medicine)
        return result.inserted_id

    def read_doctor(self, query={}):
        result = self.doctors.find(query)
        return [doctor for doctor in result]

    def read_patient(self, query={}):
        result = self.patients.find(query)
        return [patient for patient in result]

    def read_medicine(self, query={}):
        result = self.medicines.find(query)
        return [medicine for medicine in result]

    def update_doctor(self, query, update):
        result = self.doctors.update_one(query, update)
        return result.modified_count

    def update_patient(self, query, update):
        result = self.patients.update_one(query, update)
        return result.modified_count

    def update_medicine(self, query, update):
        result = self.medicines.update_one(query, update)
        return result.modified_count

    def delete_doctor(self, query):
        result = self.doctors.delete_one(query)
        return result.deleted_count

    def delete_patient(self, query):
        result = self.patients.delete_one(query)
        return result.deleted_count

    def delete_medicine(self, query):
        result = self.medicines.delete_one(query)
        return result.deleted_count

set-2

1.)from flask import Flask, redirect, url_for, render_template, request, flash

import os
from os.path import join, dirname
from dotenv import load_dotenv
import braintree
from gateway import generate_client_token, transact, find_transaction

load_dotenv()

app = Flask(name)
app.secret_key = os.environ.get('APP_SECRET_KEY')

PORT = int(os.environ.get('PORT', 4567))

TRANSACTION_SUCCESS_STATUSES = [
    braintree.Transaction.Status.Authorized,
    braintree.Transaction.Status.Authorizing,
    braintree.Transaction.Status.Settled,
    braintree.Transaction.Status.SettlementConfirmed,
    braintree.Transaction.Status.SettlementPending,
    braintree.Transaction.Status.Settling,
    braintree.Transaction.Status.SubmittedForSettlement
]

@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('new_checkout'))

@app.route('/checkouts/new', methods=['GET'])
def new_checkout():
    client_token = generate_client_token()
    return render_template('checkouts/new.html', client_token=client_token)

@app.route('/checkouts/<transaction_id>', methods=['GET'])
def show_checkout(transaction_id):
    transaction = find_transaction(transaction_id)
    result = {}
    if transaction.status in TRANSACTION_SUCCESS_STATUSES:
        result = {
            'header': 'Sweet Success!',
            'icon': 'success',
            'message': 'Your test transaction has been successfully processed. See the Braintree API response and try again.'
        }
    else:
        result = {
            'header': 'Transaction Failed',
            'icon': 'fail',
            'message': 'Your test transaction has a status of ' + transaction.status + '. See the Braintree API response and try again.'
        }

    return render_template('checkouts/show.html', transaction=transaction, result=result)

@app.route('/checkouts', methods=['POST'])
def create_checkout():
    result = transact({
        'amount': request.form['amount'],
        'payment_method_nonce': request.form['payment_method_nonce'],
        'options': {
            "submit_for_settlement": True
        }
    })

    if result.is_success or result.transaction:
        return redirect(url_for('show_checkout',transaction_id=result.transaction.id))
    else:
        for x in result.errors.deep_errors: flash('Error: %s: %s' % (x.code, x.message))
        return redirect(url_for('new_checkout'))

if name == 'main':
    app.run(host='0.0.0.0', port=PORT, debug=True)

class BankAccount:
    def init(self, acno, acname, mobile_number, balance=0):
        self.acno = acno
        self.acname = acname
        self.mobile_number = mobile_number
        self.balance = balance

    def deposit(self, x):
        self.balance += x

    def withdraw(self, y):
        if self.balance < y:
            print("Insufficient balance")
        else:
            self.balance -= y

    def getdetails(self):
        print("Account number:", self.acno)
        print("Account name:", self.acname)
        print("Mobile number:", self.mobile_number)
        print("Balance:", self.balance)

2.)A decorator is a function that takes in another function as a parameter and then returns a function.
This is possible because Python gives functions special status.
A function can be used as a parameter and a return value, while also being assigned to a variable
The Request, in Flask, is an object that contains all the data sent from the Client to Server. This data can be recovered using the GET/POST Methods.

3.)Sudder School: pip install Flask
Sudder School: from flask import Flask, render_template, request, redirect, url_for

app = Flask(name)

# Define a route for the login page
@app.route('/')
def login():
    return render_template('login.html')

# Define a route for the student details page
@app.route('/student_details')
def student_details():
    # TODO: Implement student details logic
    return render_template('student_details.html')

if name == 'main':
    app.run(debug=True)
[2/15, 10:03 AM] Sudder School: <!DOCTYPE html>
<html>
  <head>
    <title>Login Page</title>
  </head>
  <body>
    <h1>Login</h1>
    <form action="{{ url_for('student_details') }}" method="POST">
      <label for="username">Username:</label>
      <input type="text" id="username" name="username"><br><br>
      <label for="password">Password:</label>
      <input type="password" id="password" name="password"><br><br>
      <input type="submit" value="Login">
    </form>
  </body>
</html>
[2/15, 10:03 AM] Sudder School: <!DOCTYPE html>
<html>
  <head>
    <title>Student Details</title>
  </head>
  <body>
    <h1>Student Details</h1>
    <p>Welcome, {{ username }}!</p>
    <p>Here are your details:</p>
    <ul>
      <li>Name: John Doe</li>
      <li>Student ID: 123456</li>
      <li>Course: Computer Science</li>
    </ul>
  </body>
</html>
[2/15, 10:03 AM] Sudder School: @app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the username and password from the form
        username = request.form['username']
        password = request.form['password']

        # TODO: Implement authentication logic
        if username == 'admin' and password == 'admin':
            return redirect(url_for('student_details', username=username))
        else:
            return render_template('login.html', error='Invalid username or password')

    # Render the login page
    return render_template('login.html')

set-3


1.)class Employee:
    # Class attribute to keep track of count
    count = 0

    def __init__(self, emp_id, first_name, last_name, department, designation, doj, mobile):
        self.emp_id = emp_id
        self.first_name = first_name
        self.last_name = last_name
        self.department = department
        self.designation = designation
        self.doj = doj
        self.mobile = mobile
        self._email = self.generate_email()  # Call the private method to generate email
        Employee.count += 1  # Increment the count whenever a new instance is created

    # Properties for first name, last name, and email
    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = value
        self._email = self.generate_email()  # Update email when first name is changed

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = value
        self._email = self.generate_email()  # Update email when last name is changed

    @property
    def email(self):
        return self._email

    # Method to generate email based on first and last name
    def generate_email(self):
        return f"{self.first_name.lower()}.{self.last_name.lower()}@company.com"

    # String representation of the instance
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.emp_id})"


# Creating instances of Employee class
emp1 = Employee("E001", "John", "Doe", "Sales", "Manager", "01-01-2022", "9999999999")
emp2 = Employee("E002", "Jane", "Doe", "Marketing", "Executive", "02-01-2022", "8888888888")

# Testing the properties and method
print(emp1.first_name)  # Output: John
print(emp1.last_name)  # Output: Doe
print(emp1.email)  # Output: john.doe@company.com
emp1.first_name = "Jack"
print(emp1.email)  # Output: jack.doe@company.com

# Testing the count
print(Employee.count)  # Output: 2

class and tested the properties, methods, and count.


2)Decorator in Python is a design pattern that allows a user to add new functionality to an existing object or function,
without modifying its original structure.
A decorator is essentially a function that takes another function as an argument and returns a new function that adds some
additional behavior to the original function.
In Python, decorators are indicated with the @ symbol.


3)
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__) \
 \
      @ app.route('/')


def index():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)

< !DOCTYPE.html >
< html >
< head >
< meta
charset = "utf-8" >
< title > Login
Page < / title >
< / head >
< body >
< h1 > Login
Page < / h1 >
< form
method = "POST"
action = "{{ url_for('login') }}" >
< input
type = "text"
name = "username"
placeholder = "Username" >
< input
type = "password"
name = "password"
placeholder = "Password" >
< input
type = "submit"
value = "Login" >
< / form >
< / body >
< / html >

students = {
    'alice': {'name': 'Alice', 'age': 21, 'major': 'Computer Science'},
    'bob': {'name': 'Bob', 'age': 22, 'major': 'Mathematics'},
    'charlie': {'name': 'Charlie', 'age': 20, 'major': 'English'}
}


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username in students and password == 'password':
        return redirect(url_for('student_details', username=username))
    else:
        return redirect(url_for('index'))

@app.route('/<username>/details')
def student_details(username):
    if username in students:
        student = students[username]
        return render_template('details.html', student=student)
    else:
        return redirect(url_for('index'))



from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

students = {
    'alice': {'name': 'Alice', 'age': 21, 'major': 'Computer Science'},
    'bob': {'name': 'Bob', 'age': 22, 'major': 'Mathematics'},
    'charlie': {'name': 'Charlie', 'age': 20, 'major': 'English'}
}


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username in students and password == 'password':
        return redirect(url_for('student_details', username=username))
    else:
        return redirect(url_for('index'))


@app.route('/<username>/details')
def student_details(username):
    if username in students:
        student = students[username]
        return render_template('details.html', student=student)
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)



import mysql.connector

# Connect to the MySQL server
cnx = mysql.connector.connect(user='your_username', password='your_password', host='your_host')
cursor = cnx.cursor()

# Create a new database
cursor.execute("CREATE DATABASE inventory_db")

# Connect to the new database
cnx = mysql.connector.connect(user='your_username', password='your_password', host='your_host', database='inventory_db')
cursor = cnx.cursor()

# Create a new table
table = """CREATE TABLE inventory_stock (
             Sno INT AUTO_INCREMENT PRIMARY KEY,
             Product_spec_name VARCHAR(255),
             Date_of_manufacturing DATE,
             MRP FLOAT(10,2),
             Invoice_bill_no INT,
             Product_manufacturer VARCHAR(255)
         )"""
cursor.execute(table)
cnx.commit()

# Close the cursor and connection
cursor.close()
cnx.close()

To apply PyTest cases on the above-mentioned database program, you can use the following steps:
Install the pytest package using pip: pip install pytest
Create a new file in your project directory with a name like test_inventory_db.py, and write test functions in it using the assert statement to test the various functions of your program that interact with the database.
Run the test using the command pytest test_inventory_db.py in the command line.
This will execute all the test functions in the test_inventory_db.py file and give the results whether passed or failed.


from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Create a new database
db = client["Hospital"]

# Create collections for Doctor, Patient, and Medicine
doctors = db["Doctors"]
patients = db["Patients"]
medicines = db["Medicines"]

# Insert data into the collections

# Doctor
new_doctor = {"name": "Dr. John Smith", "specialization": "Surgeon", "experience": "5"}
doctors.insert_one(new_doctor)

# Patient
new_patient = {"name": "Jane Doe", "age": 25, "gender": "Female", "disease": "Fever"}
patients.insert_one(new_patient)

# Medicine
new_medicine = {"name": "Paracetamol", "dose": "500mg", "quantity": 100}
medicines.insert_one(new_medicine)

# Close the connection
client.close()


1.

from flask import Flask, render_template, request
import csv

app = Flask(__name__)

@app.route('/')
def index():
    # Read the CSV file
    presidents = []
    with open('presidents.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            presidents.append(row[0])
    # Pass the list of presidents to the template
    return render_template('index.html', presidents=presidents)

@app.route('/president/<name>')
def president(name):
    # Read the CSV file
    presidents = []
    with open('presidents.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Name'] == name:
                president = row
                break
    # Pass the president's details to the template
    return render_template('president.html', president=president)

if __name__ == '__main__':
    app.run(debug=True)

2.

from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["bookstore"]
books = db["books"]

@app.route('/')
def index():
    # Get the page number from the request
    page = int(request.args.get('page', 1))
    # Find books with available books count less than 5
    all_books = books.find({"AvailableBooksCount": {"$lt": 5}})
    # Apply pagination
    books_data = all_books.skip((page-1)*5).limit(5)
    # Pass the books data to the template
    return render_template('index.html', books=books_data)

if __name__ == '__main__':
    app.run(debug=True)
