from flask import Blueprint, jsonify, render_template, request, redirect, flash, session, url_for
import utils.db_connection as db_connection
from datetime import date
employee_bp = Blueprint('employee', __name__)

@employee_bp.route('/dashboard')
def employee_dashboard():
    if 'role' in session and session['role'] == 'employee':
        return render_template('employee_dashboard.html')
    else:
        return "Unauthorized access", 403

@employee_bp.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if 'role' in session and session['role'] == 'employee':
        if request.method == 'POST':
            customer_name = request.form['customer_name']
            customer_email = request.form['customer_email']

            conn = db_connection.get_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO customers (name, email) VALUES (%s, %s)', (customer_name, customer_email))
            conn.commit()
            conn.close()

            flash("Customer added successfully!")
            return redirect(url_for('employee.add_customer'))

        return render_template('add_cus_em.html')
    else:
        return "Unauthorized access", 403

@employee_bp.route('/purchase_product', methods=['GET', 'POST'])
def purchase_product():
    conn = db_connection.get_connection()
    cursor = conn.cursor()
    if 'role' in session and session['role'] == 'employee':
        if request.method == 'POST':
            customer_id = request.form['customer_id']
            total_amount = request.form.get('total_amount')
            if not customer_id or not total_amount:
                return jsonify({"error": "Missing required fields: customer_id or total_amount"}), 400
        
            if customer_id.strip() == '':
                print("Customer ID is missing.")
                return "Customer ID is required.", 400
        
            if total_amount.strip() == '' or float(total_amount) <= 0:
                print("Total amount is invalid or zero.")
                return "Total amount must be greater than zero.", 400
            
            invoice_date = date.today()
            cursor.execute("""
                INSERT INTO invoice (customer_id, invoice_date, total_amount)
                VALUES (%s, %s, %s)
            """, (customer_id, invoice_date, total_amount))
            items = request.form.getlist('productList[]')
            if not items:
                return jsonify({"error": "No products selected"}), 400
            for item in items:
                product_data = item.split(',')  # Assuming product and quantity are passed in a string like "product_id,quantity"
                product_id = product_data[0].strip()
                quantity = int(product_data[1].strip())

                if not product_id or quantity <= 0:
                    return jsonify({"error": f"Invalid product ID or quantity for product {product_id}"}), 400
                cursor.execute('INSERT INTO purchases (customer_id, product_id, quantity) VALUES (%s, %s, %s)', (customer_id, product_id, quantity))
            
            conn.commit()
            
            cursor.close()
            conn.close()

            flash("Product purchased successfully!")
            return redirect(url_for('employee.purchase_product'))

        else:# Fetch customers and products for dropdowns
            
            cursor.execute('SELECT id, name FROM customers')
            customers = cursor.fetchall()
            
            cursor.execute('SELECT id, name,price FROM products')
            products = cursor.fetchall()
            
            cursor.close()
            conn.close()

            return render_template('purem.html', customers=customers, products=products)
    else:
        return "Unauthorized access", 403
