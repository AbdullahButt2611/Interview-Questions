# Join Query on 3 Tables

Let's consider a scenario with three tables: `employees`, `departments`, and `salaries`. The employees table contains information about employees, the departments table contains details about different departments, and the salaries table stores salary information for each employee.

Here's an example query that joins these tables to retrieve employee names, department names, and their corresponding salaries:

```sql
SELECT employees.employee_id, employees.employee_name, departments.department_name, salaries.salary
FROM employees
JOIN departments ON employees.department_id = departments.department_id
JOIN salaries ON employees.employee_id = salaries.employee_id;
```

In this example:

- The `employees` table has columns `employee_id`, `employee_name`, and `department_id`.
- The `departments` table has columns `department_id` and `department_name`.
- The `salaries` table has columns `employee_id` and `salary`.
- The query joins these tables using the common columns: `employees.department_id = departments.department_id` and `employees.employee_id = salaries.employee_id`. This allows us to retrieve information about employees, their respective departments, and their salaries.