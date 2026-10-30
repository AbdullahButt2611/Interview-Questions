# Sort an Array Based on the Order of Another Array

`Visnext` • `Amazon` • `Meta`

## Problem Statement

You are given two arrays, `num` and `index`, that have the same length.

- Every number in `num` has a matching value in `index`.
- The value `index[i]` tells you the exact final position where `num[i]` should be placed.

Your job is to rearrange `num` so that every number sits at the position its `index` value points to, and then return this new array.

## Examples

**Example 1**

```ini
Input:  num = [50, 20, 40, 10, 30], index = [3, 1, 4, 0, 2]
Output: [10, 20, 30, 50, 40]

Explanation:
50 goes to position 3
20 goes to position 1
40 goes to position 4
10 goes to position 0
30 goes to position 2
```

**Example 2**

```ini
Input:  num = [1, 2, 3], index = [2, 0, 1]
Output: [2, 3, 1]

Explanation:
1 goes to position 2
2 goes to position 0
3 goes to position 1
```

## Constraints

- `num.length == index.length == n`
- `1 <= n <= 10^5`
- `0 <= index[i] < n`
- All values in `index` are unique.

<br><br>

## Approach 1: Direct Placement

The best move here is to stop thinking about "sorting" and start thinking about "seating".

<mark>Each number already knows its final seat. We are not comparing or sorting anything, we are just sending every number to the seat its index prints.</mark>

Here is the plain idea:

- Create a fresh empty array (call it `result`) that is the same size as `num`.
- Walk through `num` one number at a time.
- For each number, look at its matching value in `index`. That value is its seat number.
- Drop that number straight into `result` at that seat.
- After every number is seated, `result` is fully arranged. Return it.

Think of a movie theater. Every person (a number) walks in holding a ticket (its index) with a seat number already printed on it. Nobody argues, nobody swaps, nobody compares tickets. Each person just walks to their printed seat and sits down. Once everyone is seated, the room is perfectly arranged.

<br><br>

### Code

```python
def sort_by_index(num, index):
    # Make an empty array the same size as num
    result = [0] * len(num)

    # Send every number to the seat its index points to
    for i in range(len(num)):
        result[index[i]] = num[i]

    return result


num = [50, 20, 40, 10, 30]
index = [3, 1, 4, 0, 2]

print(sort_by_index(num, index))  # [10, 20, 30, 50, 40]
```

<br><br>

### Dry Run

```ini
Input:
num   = [50, 20, 40, 10, 30]
index = [3,  1,  4,  0,  2]

Start:
result = [0, 0, 0, 0, 0]   (empty array, same size as num)


Iteration 1  ->  i = 0
    num[i]   = num[0]   = 50
    index[i] = index[0] = 3
    Meaning: 50 must sit at position 3
    Action:  result[3] = 50
    result = [0, 0, 0, 50, 0]


Iteration 2  ->  i = 1
    num[i]   = num[1]   = 20
    index[i] = index[1] = 1
    Meaning: 20 must sit at position 1
    Action:  result[1] = 20
    result = [0, 20, 0, 50, 0]


Iteration 3  ->  i = 2
    num[i]   = num[2]   = 40
    index[i] = index[2] = 4
    Meaning: 40 must sit at position 4
    Action:  result[4] = 40
    result = [0, 20, 0, 50, 40]


Iteration 4  ->  i = 3
    num[i]   = num[3]   = 10
    index[i] = index[3] = 0
    Meaning: 10 must sit at position 0
    Action:  result[0] = 10
    result = [10, 20, 0, 50, 40]


Iteration 5  ->  i = 4
    num[i]   = num[4]   = 30
    index[i] = index[4] = 2
    Meaning: 30 must sit at position 2
    Action:  result[2] = 30
    result = [10, 20, 30, 50, 40]


Loop ends (every number is now seated)

Output:
result = [10, 20, 30, 50, 40]
```

<br><br>

## Approach 2: Pair and Sort

This approach keeps each number glued to its own index, then lets sorting do the arranging for us.

<mark>The key idea is that if a number always travels together with its index, then sorting by the index automatically puts every number in the right order.</mark>

Here is the plain idea:

- Pair every index value with its number so they travel together as one unit. For example, index `3` and number `50` become the pair `(3, 50)`.
- Sort all these pairs by their index value (the first item in each pair). Small index values come first, large ones come last.
- Once sorted, the pairs are already in the correct order. Pull out just the numbers (the second item of each pair) and that is your final arranged array.

Think of students each holding a card with their roll number (the index). We ask them to line up in order of their roll number. Once they are lined up, we simply read off their names in that order.

<br><br>

### Code

```python
def sort_by_index(num, index):
    # Glue each index to its number so they travel together
    paired = list(zip(index, num))

    # Sort the pairs by the index value (the first item)
    paired.sort()

    # Pull out only the numbers, now in the correct order
    result = [value for _, value in paired]

    return result


num = [50, 20, 40, 10, 30]
index = [3, 1, 4, 0, 2]

print(sort_by_index(num, index))  # [10, 20, 30, 50, 40]
```

<br><br>

### Dry Run

```ini
Input:
num   = [50, 20, 40, 10, 30]
index = [3,  1,  4,  0,  2]


Step 1: Pair each index with its number
    index[0]=3, num[0]=50  ->  (3, 50)
    index[1]=1, num[1]=20  ->  (1, 20)
    index[2]=4, num[2]=40  ->  (4, 40)
    index[3]=0, num[3]=10  ->  (0, 10)
    index[4]=2, num[4]=30  ->  (2, 30)
    paired = [(3, 50), (1, 20), (4, 40), (0, 10), (2, 30)]


Step 2: Sort the pairs by the first value (the index)
    Before: [(3, 50), (1, 20), (4, 40), (0, 10), (2, 30)]
    After:  [(0, 10), (1, 20), (2, 30), (3, 50), (4, 40)]


Step 3: Pull out only the numbers (the second value of each pair)
    (0, 10)  ->  10
    (1, 20)  ->  20
    (2, 30)  ->  30
    (3, 50)  ->  50
    (4, 40)  ->  40
    result = [10, 20, 30, 50, 40]


Output:
result = [10, 20, 30, 50, 40]
```

<br><br>

## Complexity

- **Approach 1 (Direct Placement):** Time O(n), Space O(n). This is the faster one, since every number is placed in a single step.
- **Approach 2 (Pair and Sort):** Time O(n log n), Space O(n). Slower because of the sorting step, but a nice alternate way to think about the problem.

<br><br>

## Related Problems

- [Shuffle String (1528)](https://leetcode.com/problems/shuffle-string/)
- [Shuffle the Array (1470)](https://leetcode.com/problems/shuffle-the-array/)
- [Relative Sort Array (1122)](https://leetcode.com/problems/relative-sort-array/)
- [Sort the People (2418)](https://leetcode.com/problems/sort-the-people/)