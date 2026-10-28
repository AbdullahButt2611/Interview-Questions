## Normalization
`I2C` `Netsol` `Technosoft`

Normalization is a process used in databases to organize data efficiently and minimize redundancy. It involves breaking down a database into smaller, related tables and defining relationships between them. The primary goals of normalization are to reduce data redundancy, prevent anomalies in data modification, and ensure data integrity.

There are several normal forms, each building upon the last, with the ultimate goal of achieving a fully normalized database schema. The most commonly used normal forms are:

1. **First Normal Form (1NF)**: Ensures that each column in a table contains atomic (indivisible) values, meaning there are no repeating groups or arrays within a single cell.

2. **Second Normal Form (2NF)**: Builds on 1NF and requires that each non-key attribute is fully functionally dependent on the entire primary key. This means that no partial dependencies exist, and all attributes rely on the entire primary key, not just part of it.

3. **Third Normal Form (3NF)**: Builds on 2NF and requires that there are no transitive dependencies. In other words, no non-key attribute should depend on another non-key attribute.

There are higher normal forms like Boyce-Codd Normal Form (BCNF) and Fourth Normal Form (4NF), but they are less commonly used in practice.

Normalization helps maintain data integrity, reduces data redundancy, and makes the database easier to maintain and update. However, it can also lead to increased complexity in queries since data is spread across multiple tables, so it's essential to strike a balance based on the specific needs of the application.
