from flask import Blueprint, render_template, request, redirect, flash, session, url_for
import utils.db_connection as db_connection

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
def admin_dashboard():
    if 'role' in session and session['role'] == 'admin':
        return render_template('admin_dashboard.html')
    else:
        return "Unauthorized access", 403

@admin_bp.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if 'role' in session and session['role'] == 'admin':
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']

            conn = db_connection.get_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO customers (name, email, phone) VALUES (%s, %s, %s)', (name, email, phone))
            conn.commit()
            conn.close()

            flash("Customer added successfully!")
            return redirect(url_for('admin.add_customer'))

        return render_template('add_cus.html')
    else:
        return "Unauthorized access", 403

@admin_bp.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if 'role' in session and session['role'] == 'admin':
        if request.method == 'POST':
            name = request.form['name']
            price = request.form['price']

            conn = db_connection.get_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO products (name, price) VALUES (%s, %s)', (name, price))
            conn.commit()
            conn.close()

            flash("Product added successfully!")
            return redirect(url_for('admin.add_product'))

        return render_template('add_product.html')
    else:
        return "Unauthorized access", 403
