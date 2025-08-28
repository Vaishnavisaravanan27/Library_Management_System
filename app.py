from flask import Flask, render_template, request
import csv
from datetime import datetime, timedelta

app = Flask(__name__)

# Sample books
books = [
    {
        'name': 'Python Basics',
        'image': 'https://via.placeholder.com/150',
        'available': True
    },
    {
        'name': 'Data Science Intro',
        'image': 'https://via.placeholder.com/150',
        'available': False
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == 'admin123':
        return render_template('home.html')
    else:
        return "Invalid credentials. Please go back and try again."

@app.route('/search', methods=['POST'])
def search():
    book_name = request.form['book_name']
    found = next((book for book in books if book['name'].lower() == book_name.lower()), None)
    return render_template('home.html', book=found)

@app.route('/borrow', methods=['POST'])
def borrow():
    student_name = request.form['student_name']
    student_id = request.form['student_id']
    book_name = request.form['book_name']

    # Set return date as 10 days from today
    return_date = (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')

    # Save to CSV
    with open('borrowed_books.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([student_name, student_id, book_name, return_date])

    # Mark book as borrowed
    for book in books:
        if book['name'] == book_name:
            book['available'] = False

    message = f'Book borrowed successfully! Return by: {return_date}'
    return render_template('home.html', book=None, message=message)

if __name__ == '__main__':
    app.run(debug=True)
