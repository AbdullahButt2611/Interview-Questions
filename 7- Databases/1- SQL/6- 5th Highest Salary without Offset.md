If you want to find the 5th highest salary without using OFFSET, you can utilize a subquery with the LIMIT and OFFSET within it. Here's an example query:

```sql
SELECT MAX(salary) AS fifth_highest_salary
FROM employees
WHERE salary NOT IN (
    SELECT salary
    FROM employees
    ORDER BY salary DESC
    LIMIT 4
);
```

This query selects the maximum salary `MAX(salary)` from the employees table where the salary is not in the top 4 salaries. The subquery within the WHERE clause orders the salaries in descending order and limits the result to the top 4 (LIMIT 4). The outer query then selects the maximum salary among the remaining salaries, effectively giving you the 5th highest salary.