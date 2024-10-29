from flask import Blueprint, jsonify, render_template, request, redirect, flash, url_for
from datetime import date
import utils.db_connection as db_connection

purchase_bp = Blueprint('purchase', __name__)

@purchase_bp.route('/purchase', methods=['GET', 'POST'])
def purchase_items():
    conn = db_connection.get_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        print(request.form)  # Debugging purpose to check form data
        
        # Retrieve customer_id and total_amount from the form
        customer_id = request.form.get('customer_id')
        total_amount = request.form.get('total_amount')
        
        # Validate that customer_id and total_amount are provided
        if not customer_id or not total_amount:
            return jsonify({"error": "Missing required fields: customer_id or total_amount"}), 400
        
        if customer_id.strip() == '':
            print("Customer ID is missing.")
            return "Customer ID is required.", 400
        
        if total_amount.strip() == '' or float(total_amount) <= 0:
            print("Total amount is invalid or zero.")
            return "Total amount must be greater than zero.", 400

        # Get the current date for the invoice
        invoice_date = date.today()

        # Insert invoice data into the invoice table
        cursor.execute("""
            INSERT INTO invoice (customer_id, invoice_date, total_amount)
            VALUES (%s, %s, %s)
        """, (customer_id, invoice_date, total_amount))

        # Retrieve the newly created invoice id
        invoice_id = cursor.lastrowid

        # Loop through the productList from the form data
        items = request.form.getlist('productList[]')
        if not items:
            return jsonify({"error": "No products selected"}), 400

        for item in items:
            product_data = item.split(',')  # Assuming product and quantity are passed in a string like "product_id,quantity"
            product_id = product_data[0].strip()
            quantity = int(product_data[1].strip())
            
            cursor.execute("SELECT stock FROM products WHERE id = %s", (product_id,))
            current_stock =cursor.fetchone()
            print(quantity,current_stock)
            if current_stock and current_stock[0] >= quantity:
                # Calculate the new stock
                new_stock = current_stock[0] - quantity
                cursor.execute("UPDATE products SET stock = %s WHERE id = %s", (new_stock, product_id))
                if not product_id or quantity <= 0:
                    return jsonify({"error": f"Invalid product ID or quantity for product {product_id}"}), 400
                 # Insert purchase details into purchases table
                cursor.execute("""
                    INSERT INTO purchases (customer_id, product_id, quantity)
                    VALUES (%s, %s, %s)
                """, (customer_id, product_id, quantity))
                conn.commit()
                # Check if the stock alert was triggered
                cursor.execute("SELECT COUNT(*) FROM stock_alerts WHERE product_id = %s", (product_id,))
                alert_count = cursor.fetchone()[0]

                if alert_count > 0:
                    flash(f"Stock alert triggered for product ID {product_id}: Stock is low!", "warning")

                
                
                cursor.close()
                conn.close()
                flash("Purchase successful! Stock has been updated.","sucess")
                return redirect(url_for('purchase.purchase_items'))
            else:
                # If there's not enough stock, show an error message
                 flash("Not enough stock available for this purchase of product .","error")
            return redirect(url_for('purchase.purchase_items'))
    else:
        # Retrieve customers and products for display in the HTML form
        cursor.execute("SELECT id, name FROM customers")
        customers = cursor.fetchall()

        cursor.execute("SELECT id, name, price FROM products")
        products = cursor.fetchall()

        cursor.close()
        conn.close()

        # Render the HTML template with customers and products data
        return render_template('purchase.html', customers=customers, products=products)
@purchase_bp.route('/alerts', methods=['GET'])
def get_stock_alerts():
    conn = db_connection.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM stock_alerts ORDER BY created_at DESC')
    alerts = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify(alerts)