# JOIN vs Subquery

## JOIN

A `JOIN` is used to combine rows from two or more tables based on a related column between them. There are different types of joins, such as INNER JOIN, LEFT JOIN, RIGHT JOIN, and FULL JOIN.

### Syntax:

```sql
SELECT columns
FROM table1
JOIN table2 ON table1.column = table2.column;
```

Example:

```sql
SELECT orders.order_id, customers.customer_name
FROM orders
JOIN customers ON orders.customer_id = customers.customer_id;
```

## Subquery

A subquery is a query nested inside another query, usually enclosed within parentheses. It can be used to retrieve data that will be used in the main query's condition or comparison.

### Syntax:

```sql
SELECT columns
FROM table
WHERE column OPERATOR (SELECT columns FROM another_table WHERE condition);
```

Example:

```sql
SELECT product_name
FROM products
WHERE category_id IN (SELECT category_id FROM categories WHERE category_name = 'Electronics');
```

## When to Use:

- **Use JOIN when you want to combine columns from different tables based on a related column.**
  
- **Use a subquery when you need to perform a comparison or condition based on the result of another query.**

## Performance Considerations:

- **JOIN is often more efficient for large datasets, as it allows the database engine to optimize the retrieval of related rows.**

- **Subqueries may be less efficient for large datasets, as they are executed for each row returned by the outer query.**
