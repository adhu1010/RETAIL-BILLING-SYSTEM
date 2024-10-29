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
            stock = request.form['stock']

            conn = db_connection.get_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO products (name, price,stock) VALUES (%s, %s, %s)', (name, price,stock))
            conn.commit()
            conn.close()

            flash("Product added successfully!")
            return redirect(url_for('admin.add_product'))

        return render_template('add_product.html')
    else:
        return "Unauthorized access", 403

@admin_bp.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if 'role' in session and session['role'] == 'admin':
        if request.method == 'POST':
            id=request.form['id']
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            role = request.form['role']

            conn = db_connection.get_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (id ,username, email, password, role) VALUES (%s, %s, %s, %s, %s)', (id, name, email, password, role))
            conn.commit()
            conn.close()

            flash("Customer added successfully!")
            return redirect(url_for('admin.add_user'))

        return render_template('add_user.html')
    else:
        return "Unauthorized access", 403
@admin_bp.route('/search_products', methods=['GET','POST'])
def search_products():
    if 'role' in session and session['role'] == 'admin':
        products=[]
        
        if request.method == 'POST':
            query = request.form["query"]
            print(query)
            conn = db_connection.get_connection()
            cursor = conn.cursor()
            if query is None or query.strip() == '':
            # Redirect to the customers page or handle the case where no query is provided
                cursor.execute("SELECT * FROM products")
                products = cursor.fetchall()    
                cursor.close()
                conn.close()
                return render_template('displaypro.html', products=products)
    
            # Assuming product name is in the second column of the products table
            cursor.execute("SELECT * FROM products WHERE name LIKE %s", ('%' + query + '%',))
            products = cursor.fetchall()

            cursor.close()
            conn.close()
        return render_template('displaypro.html', products=products)
    else:
        return "Unauthorized Access", 403

@admin_bp.route('/search_customers', methods=['GET','POST'])
def search_customers():
    if 'role' in session and session['role'] == 'admin':
        customers=[]
        if request.method == 'POST':
            query = request.form["query"]
            print(query)
            if query is None or query.strip() == '':
             # Redirect to the customers page or handle the case where no query is provided
                flash("Please enter a search term.", "error")
                return redirect(url_for('admin.search_customers'))

            conn = db_connection.get_connection()
            cursor = conn.cursor()
    
            # Assuming product name is in the second column of the products table
            cursor.execute("SELECT * FROM customers WHERE name LIKE %s" , ('%' + query + '%',))
            customers = cursor.fetchall()
            print(customers)
            cursor.close()
            conn.close()
        return render_template('displaycus.html', customers=customers)
    else:
        return "Unauthorized Access", 403
