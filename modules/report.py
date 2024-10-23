from flask import Blueprint, render_template, session, request
import utils.db_connection as db_connection
from datetime import datetime, timedelta

report_bp = Blueprint('report', __name__)

@report_bp.route('/report', methods=['GET', 'POST'])
def report():
    if 'role' in session and session['role'] == 'admin':
        conn = db_connection.get_connection()
        cursor = conn.cursor()

        # Default to today's date if no range is provided
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        if not start_date or not end_date:
            today = datetime.now()
            start_date = today.strftime('%Y-%m-%d')
            end_date = today.strftime('%Y-%m-%d')

        # Prepare the SQL query to filter based on date range
        query = """
            SELECT customers.name AS customer_name, products.name AS product_name, purchases.quantity, purchases.purchase_date
            FROM purchases
            JOIN customers ON purchases.customer_id = customers.id
            JOIN products ON purchases.product_id = products.id
            WHERE DATE(purchases.purchase_date) BETWEEN %s AND %s
        """
        cursor.execute(query, (start_date, end_date))
        report_data = cursor.fetchall()
        conn.close()

        return render_template('report.html', report_data=report_data, start_date=start_date, end_date=end_date)
    else:
        return "Unauthorized access", 403

