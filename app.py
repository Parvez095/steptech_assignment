from flask import Flask, render_template, request, redirect

import mysql.connector
from mysql.connector import Error

db_config = {
    'host': 'localhost',
    'user': 'root',
    'database': 'users_data'
}

app = Flask(__name__)

@app.route('/hello')
def hello():
    return "Hello, World!"

@app.route('/users')
def users():
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Retrieve users from the database
        query = "SELECT * FROM users"
        cursor.execute(query)
        users = cursor.fetchall()

        # Close the database connection
        cursor.close()
        conn.close()

        return render_template('users.html', users=users)
    except Error as e:
        # Handle MySQL connection or query error
        error_message = "Error occurred while retrieving users from the database: {}".format(e)
        return render_template('error.html', error_message=error_message)

@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    error_message = None

    if request.method == 'POST':
        # Retrieve the user input from the form
        name = request.form['name']
        email = request.form['email']
        role = request.form['role']

        try:
            # Connect to MySQL database
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Check if the email already exists in the database
            query = "SELECT COUNT(*) FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            count = cursor.fetchone()[0]

            if count > 0:
                # Email already exists, display an error message
                error_message = "Email already exists in the database."
            else:
                # Insert the new user data into the database
                query = "INSERT INTO users (name, email, role) VALUES (%s, %s, %s)"
                values = (name, email, role)
                cursor.execute(query, values)
                conn.commit()

                # Redirect to the /users route to display the updated user list
                return redirect('/users')
        except Error as e:
            # Handle MySQL connection or query error
            error_message = "Error occurred while adding a new user to the database: {}".format(e)
        
        # Close the database connection
        cursor.close()
        conn.close()

    # Render the HTML template for the new_user form
    return render_template('new_user.html', error_message=error_message)

@app.route('/users/<id>')
def user_details(id):
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Retrieve the details of the specific user from the database
        query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(query, (id,))
        user = cursor.fetchone()

        # Close the database connection
        cursor.close()
        conn.close()

        if user:
            # User found, display the user details
            return render_template('user_details.html', user=user)
        else:
            # User not found, display an error message
            error_message = "User with ID {} not found.".format(id)
            return render_template('error.html', error_message=error_message)
    except Error as e:
        # Handle MySQL connection or query error
        error_message = "Error occurred while retrieving user details from the database: {}".format(e)
        return render_template('error.html', error_message=error_message)

@app.route('/error')
def error():
    # Route to display a generic error page
    return render_template('error.html', error_message="An error occurred.")

if __name__ == '__main__':
    app.run()
