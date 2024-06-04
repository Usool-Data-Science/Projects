-- Create the database
CREATE DATABASE grocery_store;

-- Use the database
USE grocery_store;

-- Create the 'uom' table
CREATE TABLE uom (
    uom_id INT AUTO_INCREMENT PRIMARY KEY,
    uom_name VARCHAR(255) NOT NULL
);

-- Create the 'products' table
CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    uom_id INT NOT NULL,
    price_per_unit DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (uom_id) REFERENCES uom(uom_id)
);

-- Create the 'orders' table
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    datetime DATETIME NOT NULL
);

-- Create the 'order_details' table
CREATE TABLE order_details (
    order_detail_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity DECIMAL(10, 2) NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Insert some sample data into 'uom' table
INSERT INTO uom (uom_name) VALUES ('Kilogram'), ('Litre'), ('Piece');

-- Insert some sample data into 'products' table
INSERT INTO products (name, uom_id, price_per_unit) VALUES ('Apple', 1, 3.50), ('Milk', 2, 1.20), ('Bread', 3, 2.00);

-- Insert some sample data into 'orders' table
INSERT INTO orders (customer_name, total, datetime) VALUES ('John Doe', 20.50, '2024-05-24 10:30:00'), ('Jane Smith', 15.75, '2024-05-24 11:00:00');

-- Insert some sample data into 'order_details' table
INSERT INTO order_details (order_id, product_id, quantity, total_price) VALUES (1, 1, 2, 7.00), (1, 3, 1, 2.00), (2, 2, 3, 3.60);
-- Insert sample data into 'uom' table
INSERT INTO uom (uom_name) VALUES
('Kilogram'),
('Litre'),
('Piece'),
('Pack'),
('Box'),
('Dozen'),
('Gram'),
('Meter'),
('Centimeter'),
('Milliliter');

-- Insert sample data into 'products' table
INSERT INTO products (name, uom_id, price_per_unit) VALUES
('Apple', 1, 3.50),
('Milk', 2, 1.20),
('Bread', 3, 2.00),
('Cheese', 4, 5.00),
('Soap', 5, 2.50),
('Eggs', 6, 0.20),
('Flour', 7, 0.50),
('Cable', 8, 1.00),
('Ruler', 9, 0.30),
('Juice', 10, 0.80);

-- Insert sample data into 'orders' table
INSERT INTO orders (customer_name, total, datetime) VALUES
('John Doe', 20.50, '2024-05-24 10:30:00'),
('Jane Smith', 15.75, '2024-05-24 11:00:00'),
('Alice Johnson', 30.00, '2024-05-24 12:15:00'),
('Bob Brown', 12.40, '2024-05-24 13:45:00'),
('Charlie Black', 25.50, '2024-05-24 14:30:00'),
('Diana White', 18.90, '2024-05-24 15:10:00'),
('Edward Green', 22.00, '2024-05-24 16:20:00'),
('Fiona Blue', 14.30, '2024-05-24 17:35:00'),
('George Yellow', 27.60, '2024-05-24 18:50:00'),
('Hannah Purple', 19.80, '2024-05-24 19:25:00');

-- Insert sample data into 'order_details' table
INSERT INTO order_details (order_id, product_id, quantity, total_price) VALUES
(1, 1, 2, 7.00),
(1, 3, 1, 2.00),
(2, 2, 3, 3.60),
(2, 4, 1, 5.00),
(3, 5, 5, 12.50),
(3, 6, 12, 2.40),
(4, 7, 10, 5.00),
(4, 8, 2, 2.00),
(5, 9, 3, 0.90),
(5, 10, 5, 4.00),
(6, 1, 4, 14.00),
(6, 2, 1, 1.20),
(7, 3, 3, 6.00),
(7, 4, 1, 5.00),
(8, 5, 2, 5.00),
(8, 6, 6, 1.20),
(9, 7, 4, 2.00),
(9, 8, 1, 1.00),
(10, 9, 7, 2.10),
(10, 10, 8, 6.40);
