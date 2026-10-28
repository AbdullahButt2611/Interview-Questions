# Explain the first and 3rd normal form in DBMS
`Netsol`

First and third normal forms (1NF and 3NF) are essential concepts in database normalization, which aims to reduce redundancy and improve data integrity in relational databases.

## First Normal Form (1NF)
A table is in First Normal Form (1NF) if it satisfies the following criteria:
- **Atomicity**: Each cell in the table must contain a single value; no cell should hold multiple values or lists.
- **Unique Rows**: Each row must be unique, meaning no two rows can be identical.
- **Single Value Columns**: Each column must contain values of a single attribute, and all entries in a column must be of the same kind.
- **Unique Column Names**: Each column must have a unique name.

These rules help eliminate duplicate data and simplify queries, making it easier to manage the database effectively
<br><br>

## Third Normal Form (3NF)
A table is in Third Normal Form (3NF) if it meets the following conditions:
- **In Second Normal Form (2NF)**: The table must first be in 2NF, which means it should not have any partial dependencies of non-key attributes on a composite primary key.
- **No Transitive Dependency**: All non-prime attributes (attributes not part of any candidate key) must be directly dependent only on the primary key and not on any other non-prime attribute. This means that if attribute A determines attribute B, then A must be a super key, ensuring that non-prime attributes do not depend on other non-prime attributes

In simpler terms, 3NF ensures that every non-key attribute is dependent solely on the primary key, which helps eliminate redundancy and potential anomalies during data operations like updates or deletions.
<br><br>

## Summary
- 1NF focuses on the structure of the table to ensure atomicity and uniqueness.
- 3NF builds on 1NF by eliminating transitive dependencies, ensuring that non-key attributes are only dependent on the primary key.

These normalization forms are crucial for designing efficient and reliable relational databases.