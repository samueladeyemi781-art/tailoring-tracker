import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    with open('schema.sql', 'r') as f:
        conn.executescript(f.read())
    conn.close()

def init_db():
    conn = get_db()
    with open('schema.sql', 'r') as f:
        conn.executescript(f.read())
    conn.close()
    init_db()
@app.route('/')
def index():
    search = request.args.get('search', '')
    conn = get_db()
    if search:
        query = '''
            SELECT orders.*, customers.name, customers.phone,
                   (orders.total_amount - orders.amount_paid) AS balance
            FROM orders
            JOIN customers ON orders.customer_id = customers.id
            WHERE customers.name LIKE ? OR customers.phone LIKE ?
            ORDER BY orders.id DESC
        '''
        orders = conn.execute(query, (f'%{search}%', f'%{search}%')).fetchall()
    else:
        query = '''
            SELECT orders.*, customers.name, customers.phone,
                   (orders.total_amount - orders.amount_paid) AS balance
            FROM orders
            JOIN customers ON orders.customer_id = customers.id
            ORDER BY orders.id DESC
        '''
        orders = conn.execute(query).fetchall()
    conn.close()
    return render_template('index.html', orders=orders, search=search)

@app.route('/add', methods=['POST'])
def add_order():
    name = request.form['name']
    phone = request.form['phone']
    style = request.form['style']
    measurements = request.form['measurements']
    fitting_date = request.form['fitting_date']
    total = float(request.form['total'])
    paid = float(request.form['paid'])

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO customers (name, phone) VALUES (?, ?)', (name, phone))
    customer_id = cursor.lastrowid
    
    cursor.execute('''
        INSERT INTO orders (customer_id, style_description, measurements, fitting_date, total_amount, amount_paid, status)
        VALUES (?, ?, ?, ?, ?, ?, 'Pending')
    ''', (customer_id, style, measurements, fitting_date, total, paid))
    
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/update_status/<int:id>', methods=['POST'])
def update_status(id):
    status = request.form['status']
    conn = get_db()
    conn.execute('UPDATE orders SET status = ? WHERE id = ?', (status, id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_order(id):
    conn = get_db()
    order = conn.execute('SELECT customer_id FROM orders WHERE id = ?', (id,)).fetchone()
    if order:
        cust_id = order['customer_id']
        conn.execute('DELETE FROM orders WHERE id = ?', (id,))
        conn.execute('DELETE FROM customers WHERE id = ?', (cust_id,))
        conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/receipt/<int:id>')
def receipt(id):
    conn = get_db()
    query = '''
        SELECT orders.*, customers.name, customers.phone,
               (orders.total_amount - orders.amount_paid) AS balance
        FROM orders
        JOIN customers ON orders.customer_id = customers.id
        WHERE orders.id = ?
    '''
    order = conn.execute(query, (id,)).fetchone()
    conn.close()
    return render_template('receipt.html', order=order)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)