# Behavior of Left Outer Join
`Tintash` `I2C`

A LEFT OUTER JOIN is a type of SQL join operation that returns all records from the left table (the table mentioned before the JOIN keyword), and the matched records from the right table (the table mentioned after the JOIN keyword). If there is no match, NULL values are returned for the columns from the right table.

> ### NULL values for non-matching rows
> If there are no matching rows in the right table, the columns from the right table in the result set will contain NULL values.

### Example

Here's an example of a LEFT OUTER JOIN:

Suppose we have two tables: `orders` and `customers`. The orders table contains information about orders, and the customers table contains information about customers who placed those orders.

```sql
SELECT orders.order_id, orders.order_date, customers.customer_name
FROM orders
LEFT OUTER JOIN customers ON orders.customer_id = customers.customer_id;
```

The result set will contain all rows from the orders table, and for each order, if there is a matching customer_id in the customers table, the corresponding customer_name will be included. If there is no matching customer_id, customer_name will be NULL for that row.