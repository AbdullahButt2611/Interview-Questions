# Difference between primary, foreign and composite keys with example
`Netsol`

<br>

Primary, foreign, and composite keys are fundamental concepts in relational databases, serving to uniquely identify records and establish relationships between tables.

<br>

## Primary Key
A primary key is a unique identifier for a record in a table. It ensures that each entry is distinct and does not accept null values. For example, in a student table, the `roll number` could serve as the primary key because it uniquely identifies each student:

| Roll Number | Student Name | Program |
|-------------|--------------|---------|
| 1001        | John Doe     | MBA     |
| 1002        | Mary Jane    | MBA     |
| 1003        | James Penny  | MCA     |

In this case, the roll number is unique for each student, making it an ideal primary key.
<br><br>

## Foreign Key
A foreign key is a column or a set of columns in one table that refers to the primary key in another table. It establishes a relationship between the two tables, ensuring referential integrity. For instance, if we have a results table that includes a roll number, that roll number would be a foreign key linking back to the student table:

| Result ID | Roll Number | Course   |
|-----------|--------------|----------|
| 1         | 1001         | DBMS     |
| 2         | 1002         | Networks |
| 3         | 1004         | AI       |


Here, the roll number in the results table is a foreign key that references the roll number in the student table, ensuring that any roll number entered in the results table corresponds to an existing student
<br><br>

## Composite Key
A composite key is a primary key that consists of two or more columns used together to uniquely identify a record. This is useful when a single column is not sufficient to ensure uniqueness. For example, if we need to uniquely identify student enrollments in different programs, we might use both roll number and program as a composite key

| Roll Number | Program | Enrollment Date |
|-------------|---------|-----------------|
| 1001        | MBA     | 2023-01-15      |
| 1001        | MCA     | 2023-01-20      |
| 1002        | MBA     | 2023-01-18      |


In this case, the combination of roll number and program serves as a composite key, allowing for multiple entries for the same roll number as long as the program differs
<br><br>

## Summary of Differences

| Key Type      | Uniqueness                       | Null Values | Relationship                                |
|---------------|----------------------------------|-------------|---------------------------------------------|
| Primary Key   | Unique per row                   | No          | Identifies records in the same table        |
| Foreign Key   | Not unique                       | Yes         | Links to primary key in another table       |
| Composite Key | Unique per combination of columns| No          | Identifies records using multiple columns   |


These keys are essential for maintaining data integrity and establishing relationships within a relational database system.