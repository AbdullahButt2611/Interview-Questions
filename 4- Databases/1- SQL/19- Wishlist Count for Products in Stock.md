# SQL Interview Question: Wishlist Count for Products in Stock

`IBM` `HackerRank`

## Problem Statement

Write an SQL query to find the name, price (with 2 decimal points), and the total number of times each product appears in the `wishlists` table. Only include products that are in stock. The results should be sorted in ascending order by product name.

Tables:

**`products`**
| id | name | price | in_stock |

**`wishlists`**
| product_id | email |

**Sample Output**

| product_name                 | price  | total_wishlist_count |
| ---------------------------- | ------ | -------------------- |
| Artisanal Home Fragrance Set | 133.28 | 20                   |
| BeautyQueen Makeup Set       | 609.16 | 20                   |
| CoffeeConnoisseur Gift Box   | 229.32 | 25                   |


## Constraints

* Only products with `in_stock = 1` should be included.
* Price should always display **2 decimal places**.
* Results should be sorted by `product_name` in ascending order.
* Count of wishlist entries should reflect **how many times the product appears in the wishlist**.


## Solution

```sql
SELECT
    p.name AS product_name,
    CAST(p.price AS DECIMAL(10,2)) AS price,
    COUNT(w.product_id) AS total_wishlist_count
FROM products AS p
JOIN wishlists AS w
    ON p.id = w.product_id
WHERE p.in_stock = 1
GROUP BY p.id, p.name, p.price
ORDER BY p.name ASC;
```

**Explanation:**

* `JOIN` links products to wishlists.
* `WHERE p.in_stock = 1` filters only available products.
* `COUNT(w.product_id)` counts wishlist occurrences.
* `CAST(p.price AS DECIMAL(10,2))` ensures trailing zeros.
* `GROUP BY p.id, p.name, p.price` includes all non-aggregated selected columns.
* `ORDER BY p.name ASC` sorts alphabetically.

**Optional Variant:** Use `LEFT JOIN` instead of `JOIN` to include in-stock products with zero wishlist entries:

```sql
SELECT
    p.name AS product_name,
    CAST(p.price AS DECIMAL(10,2)) AS price,
    COUNT(w.product_id) AS total_wishlist_count
FROM products AS p
LEFT JOIN wishlists AS w
    ON p.id = w.product_id
WHERE p.in_stock = 1
GROUP BY p.id, p.name, p.price
ORDER BY p.name ASC;
```

This variant ensures that products in stock but not in any wishlist are also included with a `total_wishlist_count` of `0`.
