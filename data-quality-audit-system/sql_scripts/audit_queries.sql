-- Data Quality Audit Queries for GlobalMart Inc.

-- Use the database
USE globalmart_dw;

-- 1. Check for missing values in critical columns
SELECT "Missing Customer Emails" AS audit_check, COUNT(*) AS issue_count
FROM customers WHERE email IS NULL OR email = "";

-- 2. Check for invalid email formats
SELECT "Invalid Email Formats" AS audit_check, COUNT(*) AS issue_count
FROM customers WHERE email NOT LIKE "%@%.%";

-- 3. Check for duplicate records
SELECT "Duplicate Customers" AS audit_check, COUNT(*) AS issue_count
FROM (
    SELECT email, COUNT(*) 
    FROM customers 
    GROUP BY email 
    HAVING COUNT(*) > 1
) AS duplicates;

-- 4. Check for orders with shipped_date before order_date
SELECT "Invalid Ship Dates" AS audit_check, COUNT(*) AS issue_count
FROM orders WHERE shipped_date < order_date;

-- 5. Check for negative quantities in order_items
SELECT "Negative Quantities" AS audit_check, COUNT(*) AS issue_count
FROM order_items WHERE quantity < 0;

-- 6. Check for products with NULL stock quantities
SELECT "Missing Stock Info" AS audit_check, COUNT(*) AS issue_count
FROM products WHERE stock_quantity IS NULL;

-- 7. Check for future dates in registration
SELECT "Future Registration Dates" AS audit_check, COUNT(*) AS issue_count
FROM customers WHERE registration_date > CURDATE();

-- 8. Check for orders with zero or negative total amounts
SELECT "Invalid Order Amounts" AS audit_check, COUNT(*) AS issue_count
FROM orders WHERE total_amount <= 0;

-- 9. Check for orphaned order items (items without orders)
SELECT "Orphaned Order Items" AS audit_check, COUNT(*) AS issue_count
FROM order_items oi
LEFT JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_id IS NULL;

-- 10. Check for customers without any orders
SELECT "Inactive Customers" AS audit_check, COUNT(*) AS issue_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;

-- Summary report of all issues
SELECT 'Data Quality Issues Summary' AS '';
SELECT 
    audit_check,
    issue_count,
    CASE 
        WHEN issue_count = 0 THEN 'PASS'
        ELSE 'FAIL'
    END AS status
FROM (
    SELECT "Missing Customer Emails" AS audit_check, COUNT(*) AS issue_count FROM customers WHERE email IS NULL OR email = ""
    UNION ALL SELECT "Invalid Email Formats", COUNT(*) FROM customers WHERE email NOT LIKE "%@%.%"
    UNION ALL SELECT "Invalid Ship Dates", COUNT(*) FROM orders WHERE shipped_date < order_date
    UNION ALL SELECT "Missing Stock Info", COUNT(*) FROM products WHERE stock_quantity IS NULL
    UNION ALL SELECT "Future Registration Dates", COUNT(*) FROM customers WHERE registration_date > CURDATE()
) AS issues
ORDER BY issue_count DESC;