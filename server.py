from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL
import re
app = Flask(__name__)
app.secret_key="keep it a secret"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    mysql = connectToMySQL('email_validation')

    unique_email_query = "SELECT COUNT(*) FROM emails WHERE email = (%(em)s);"

    data = {
        'em': request.form['email']
    }    
    db_response = mysql.query_db(unique_email_query, data) 
    if not EMAIL_REGEX.match(request.form['email']):
        flash('Email is invalid!')
    elif len(db_response)> 0:
        flash('Email already exists!')
    else:
        mysql = connectToMySQL('email_validation')

        query = "INSERT INTO emails (email) VALUES (%(em)s);"
        data = {
            'em': request.form['email']
        }
        mysql.query_db(query, data)
        flash("Email Added Thank You!")
        return redirect('/success')
    return redirect('/')

@app.route('/success')
def success():
    mysql = connectToMySQL('email_validation')
    query = "SELECT * FROM emails;"
    emails = mysql.query_db(query)
    return render_template('success.html', all_emails= emails)
    



if __name__ =="__main__":
    app.run(debug=True)