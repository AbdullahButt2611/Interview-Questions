# Clustered Indexing
`Technosoft`
<br><br>

A **clustered index** is a type of database index that sorts and stores the rows of data in the table based on the index key's values. In a clustered index, the actual data rows are stored in the same order as the index, making it efficient for retrieving a range of values or for queries that require sorting.

## Key Points
1. **Only One Per Table**: Since the data rows are physically sorted, there can be only one clustered index per table. This is usually applied to the primary key.
   
2. **Faster Data Retrieval**: Clustered indexes are beneficial when you need to retrieve rows in a specific order, as the data is stored in the index order directly. For example, range-based searches are more efficient with a clustered index.

3. **Updates and Insertions Impact**: Because the data is physically ordered, inserting or updating a row that disrupts the order may involve rearranging rows. This can make these operations slightly slower in tables with a clustered index, particularly for large datasets.

4. **Comparison to Non-Clustered Indexes**: Unlike clustered indexes, non-clustered indexes store a separate structure for the index and include a pointer to the actual data row. Non-clustered indexes can be multiple in a table, as they don’t alter the physical order of the rows.

## Example
Suppose you have a table of `Customers` with a clustered index on the `CustomerID` column (the primary key). This means the data rows are sorted by `CustomerID`, allowing faster access if you need to find a customer by their ID.

---

Would you like further details on clustered indexing, or should I expand on non-clustered indexing as well?
