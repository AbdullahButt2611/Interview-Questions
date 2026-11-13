# Perform Right Outer Join Using Left

A right outer join can be achieved using a left outer join by swapping the positions of the tables. In a right outer join, all records from the right table are included, and matching records from the left table are included. If there is no match, NULL values are included for the columns from the left table.

```sql
-- Assuming you have two tables: TableA and TableB
-- Perform a right outer join using a left outer join

SELECT *
FROM TableB
LEFT OUTER JOIN TableA ON TableB.id = TableA.id;
```

In this example, `TableB` is on the left side of the LEFT OUTER JOIN, and `TableA` is on the right side. This effectively gives you the result of a right outer join where all records from `TableB` are included, and matching records from TableA are included, along with `NULL` values for non-matching columns from `TableA`.