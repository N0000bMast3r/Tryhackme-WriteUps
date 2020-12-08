from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:PurpleElephants90!@localhost/duckyinc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
eng = create_engine('mysql+pymysql://root:PurpleElephants90!@localhost/duckyinc')


# Main Index Route
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html', title='Home')


# Contact Route
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash('Thank you for reaching out.  Someone will be in touch shortly.')
        return render_template('contact.html', title='Contact')

    elif request.method == 'GET':
        return render_template('contact.html', title='Contact')


# Products Route
@app.route('/products', methods=['GET'])
def products():
    return render_template('products.html', title='Our Products')


# Product Route
# SQL Query performed here
@app.route('/products/<product_id>', methods=['GET'])
def product(product_id):
    with eng.connect() as con:
        # Executes the SQL Query
        # This should be the vulnerable portion of the application
        rs = con.execute(f"SELECT * FROM product WHERE id={product_id}")
        product_selected = rs.fetchone()  # Returns the entire row in a list
    return render_template('product.html', title=product_selected[1], result=product_selected)


# Login
@app.route('/login', methods=['GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html', title='Customer Login')


# Admin login
@app.route('/admin', methods=['GET'])
def admin():
    if request.method == 'GET':
        return render_template('admin.html', title='Admin Login')


# Page Not found error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', error=e), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', error=e), 500


if __name__ == "__main__":
    app.run('0.0.0.0')
