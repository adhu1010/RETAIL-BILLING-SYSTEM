# In modules/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import utils.db_connection as db_connection
import time as t

auth_bp = Blueprint('auth', __name__)
@auth_bp.route('/')
def home():
    return render_template('home.html')  # Render homepage

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle form data
        username = request.form['username']
        password = request.form['password']
        user = db_connection.get_user(username, password)
        if user:
            session['username'] = username
            session['role'] = user['role']
            if user['role'] == 'admin':
                return redirect(url_for('admin.admin_dashboard'))
            elif user['role']== 'employee':
                return redirect(url_for('employee.employee_dashboard'))
        else:
            flash("Invalid Username or Password ","error")
            return redirect(url_for('auth.login'))

    # Render the login page for GET requests
    return render_template('login.html')
