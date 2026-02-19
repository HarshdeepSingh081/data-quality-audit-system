-- Use the database
USE globalmart_dw;

-- Insert sample customers (with some data quality issues)
INSERT INTO customers VALUES
(1001, "John", "Doe", "john.doe@email.com", "1234567890", "123 Main St", "New York", "USA", "2023-01-15", "Active"),
(1002, "Jane", "Smith", "invalid-email", NULL, "456 Oak Ave", "Los Angeles", "USA", "2023-02-20", "Active"),
(1003, NULL, "Johnson", "bob.johnson@email.com", "9876543210", NULL, "Chicago", "USA", "2023-03-10", "Inactive"),
(1004, "Alice", "Brown", "alice.b@email.com", "5551234567", "789 Pine Rd", "Houston", "USA", "2023-01-05", "Active"),
(1005, "Charlie", NULL, "charlie@email.com", "7778889999", "321 Elm St", "Phoenix", "USA", "2023-04-12", "Active");

-- Insert sample products
INSERT INTO products VALUES
(2001, "Laptop Pro", "Electronics", 5001, 999.99, 50, 10, FALSE),
(2002, "Wireless Mouse", "Electronics", 5001, 29.99, 200, 25, FALSE),
(2003, "Desk Chair", "Furniture", 5002, 199.99, NULL, 5, FALSE),
(2004, "Coffee Maker", "Appliances", 5003, 79.99, 30, 8, FALSE),
(2005, "Notebook Set", "Stationery", 5004, 12.99, 500, 50, FALSE);

-- Insert sample orders (with date issues)
INSERT INTO orders VALUES
(3001, 1001, "2024-01-10 10:30:00", "2024-01-12 14:20:00", "Delivered", 1029.98),
(3002, 1002, "2024-01-15 09:15:00", NULL, "Processing", 42.98),
(3003, 1003, "2024-01-20 16:45:00", "2024-01-18 11:30:00", "Shipped", 212.98),
(3004, 1001, "2024-01-25 11:00:00", "2024-01-27 10:00:00", "Delivered", 79.99),
(3005, 1005, "2024-02-01 14:20:00", "2024-02-03 09:45:00", "Delivered", 25.98);

-- Insert sample order items
INSERT INTO order_items VALUES
(4001, 3001, 2001, 1, 999.99, 0.00),
(4002, 3001, 2002, 1, 29.99, 0.00),
(4003, 3002, 2002, 1, 29.99, 0.00),
(4004, 3002, 2005, 1, 12.99, 0.00),
(4005, 3003, 2003, 1, 199.99, 0.00),
(4006, 3003, 2005, 1, 12.99, 0.00),
(4007, 3004, 2004, 1, 79.99, 0.00),
(4008, 3005, 2002, 1, 25.98, 0.00);

-- Verify data insertion
SELECT 'Customers' AS table_name, COUNT(*) AS record_count FROM customers
UNION ALL
SELECT 'Products', COUNT(*) FROM products
UNION ALL
SELECT 'Orders', COUNT(*) FROM orders
UNION ALL
SELECT 'Order Items', COUNT(*) FROM order_items;