CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    style_description TEXT NOT NULL,
    measurements TEXT NOT NULL,
    fitting_date DATE,
    total_amount REAL NOT NULL,
    amount_paid REAL NOT NULL,
    status TEXT DEFAULT 'Pending',
    FOREIGN KEY(customer_id) REFERENCES customers(id)
);

-- Pre-load Demo Data
INSERT INTO customers (name, phone) VALUES ('John Doe', '08012345678');
INSERT INTO orders (customer_id, style_description, measurements, fitting_date, total_amount, amount_paid, status)
VALUES (1, 'Native Senator Suit (Blue)', 'Chest: 40", Waist: 34"', '2026-11-10', 25000, 15000, 'Fitting');