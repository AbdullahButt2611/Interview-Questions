# 4th Max Salary?

Finding the 4th maximum salary typically involves ordering the salaries in descending order and then selecting the 4th row.

### Why did you use `DISTINCT` in query?

Using the `DISTINCT` keyword in the query ensures that duplicate salary values are considered only once, which is important when dealing with salary data.

Here's an example SQL query using the DISTINCT keyword to find the 4th maximum salary:

```sql
SELECT DISTINCT salary
FROM employees
ORDER BY salary DESC
LIMIT 1 OFFSET 3;
```

### Any other way to find 4th max?

If you don't use DISTINCT, and there are duplicate salary values in the table, it might affect the result. The DISTINCT keyword ensures that you get unique salary values.

Alternatively, you can use the OFFSET and FETCH clauses if your database system supports them:

```sql
SELECT salary
FROM employees
ORDER BY salary DESC
OFFSET 3 ROWS FETCH NEXT 1 ROW ONLY;
```
