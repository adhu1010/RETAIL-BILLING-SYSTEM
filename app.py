from flask import Flask
from modules.auth import auth_bp
from modules.admin import admin_bp
from modules.purchase import purchase_bp
from modules.report import report_bp
from modules.invoice_report import invoice_report_bp
from modules.employee_dashboard import employee_bp

app = Flask(__name__)
app.secret_key = 'dbms'

# Register Blueprints
app.register_blueprint(employee_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(purchase_bp)
app.register_blueprint(report_bp, url_prefix='/admin')
app.register_blueprint(invoice_report_bp)
if __name__ == "__main__":
    app.run(debug=True)
