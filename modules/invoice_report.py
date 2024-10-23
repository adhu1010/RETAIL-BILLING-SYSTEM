from flask import Blueprint, render_template, session, request
import utils.db_connection as db_connection
from datetime import datetime

invoice_report_bp = Blueprint('invoice_report', __name__)

@invoice_report_bp.route('/invoice_report', methods=['GET', 'POST'])
def invoice_report():
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

        # Query to fetch invoice data along with total sales amount
        query = """
            SELECT invoice.invoice_id, invoice.total_amount, invoice.invoice_date,customers.name AS customer_name
            FROM customers JOIN invoice on customers.id = invoice.customer_id
            WHERE DATE(invoice.invoice_date) BETWEEN %s AND %s
        """
        cursor.execute(query, (start_date, end_date))
        invoice_report_data = cursor.fetchall()
        conn.close()

        return render_template('report.html', invoice_report_data=invoice_report_data, start_date=start_date, end_date=end_date)
    else:
        return "Unauthorized access", 403
