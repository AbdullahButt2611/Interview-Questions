# Book Allocation Problem

`Google` • `Amazon` • `Microsoft` • `Flipkart` • `TCS` • `IBM` • `PayU` • `Codenation` • `takeUforward`

## Problem Statement

You are given an array `nums` of `n` integers, where `nums[i]` represents the number of pages in the i-th book, and an integer `m` representing the number of students.

Allocate all the books to the students such that:

- Each student gets **at least one** book.
- Each book is given to **only one** student.
- The allocation is **contiguous** (a student cannot get book 1 and book 3 while skipping book 2).

Allocate the books to `m` students in such a way that the **maximum number of pages assigned to a student is minimized**.

If the allocation of books is not possible, return `-1`.

## Examples

**Example 1**

```ini
Input : nums = [12, 34, 67, 90], m = 2
Output: 113
```

All the possible ways to split these 4 books between 2 students:

- `12 | 34, 67, 90` → max(12, 191) = 191
- `12, 34 | 67, 90` → max(46, 157) = 157
- `12, 34, 67 | 90` → max(113, 90) = 113

The smallest of these maximums is `113`, so the answer is `113`.

**Example 2**

```ini
Input : nums = [25, 46, 28, 49, 24], m = 4
Output: 71
```

The best split is `25, 46 | 28 | 49 | 24`, giving loads of 71, 28, 49 and 24, so the maximum is `71`.

No other split of these 5 books among 4 students has a maximum smaller than 71.

## Constraints

- `1 <= n <= 10^5`
- `1 <= nums[i] <= 10^4`
- `1 <= m <= 10^5`

<br><br>

## Intuition

- Imagine someone tells you, "no student is allowed to read more than 100 pages". You can check that promise very quickly.
- Walk through the books from left to right, keep piling pages onto the current student, and the moment the pile would cross 100, hand that book to a **new** student instead.
- Whatever count you end up with is the **minimum number of students** needed for the limit 100.
- Now look at how that count behaves:
  - A **bigger** page limit means each student can hold more books, so **fewer** students are needed.
  - A **smaller** page limit means each student holds less, so **more** students are needed.
- This behaviour is one directional, and that is exactly the situation binary search loves.
- So instead of searching inside the array, we binary search on the **answer itself**, which is the maximum pages a single student is allowed to read.

<mark>The answer always lies between max(nums) and sum(nums).</mark> It cannot be smaller than the biggest single book (someone must read that whole book), and it cannot be bigger than the total pages (one student reading everything).

<br><br>

## Approach

**Step 1: Handle the impossible case**

- If the number of books is less than the number of students (`n < m`), at least one student gets nothing, so return `-1` right away.

**Step 2: Fix the search space**

- `low = max(nums)` (the smallest limit that is even meaningful)
- `high = sum(nums)` (the largest limit that is ever needed)
- `ans = infinity` to remember the best valid limit found so far

**Step 3: Binary search on the answer**

While `low <= high`:

- Take `mid = (low + high) // 2` and treat it as the rule "no student reads more than `mid` pages".
- Count how many students that rule needs:
  - Start with `students = 1` and `pageCount = 0`.
  - For every book in order:
    - If `pageCount + book <= mid`, the book still fits with the current student, so do `pageCount += book`.
    - Otherwise the current student is full, so do `students += 1` and `pageCount = book` (the new student begins with this book).
- Now compare that count with `m`:
  - `students == m` → `mid` is a valid answer, so save it in `ans` and then try to do even better by moving left with `high = mid - 1`.
  - `students > m` → `mid` is too small, the books are being cut into too many pieces, so raise the limit with `low = mid + 1`.
  - `students < m` → `mid` is too generous, we finished with spare students, so lower the limit with `high = mid - 1`.

**Step 4: Return the result**

- When the loop ends, `ans` holds the smallest limit that could be achieved with exactly `m` students.

<br><br>

## Code

```python
class Solution:
    def findStudentsAllocated(self, nums, pages):
        students = 1
        pageCount = 0

        for num in nums:
            if pageCount + num <= pages:
                pageCount += num
            else:
                students += 1
                pageCount = num
        
        return students


    def findPages(self, nums, m):
        if len(nums) < m:
            return -1

        low = max(nums)
        high = sum(nums)
        ans = float('inf')

        while low <= high:
            mid = (low + high) // 2
            students = self.findStudentsAllocated(nums, mid)

            if students == m: 
                ans = mid

            if students > m:
                low = mid + 1
            else:
                high = mid - 1
        
        return ans
```

<br><br>

## Dry Run

```ini
Input : nums = [25, 46, 28, 49, 24], m = 4

SETUP
n = 5, m = 4  ->  n >= m, so the allocation is possible
low  = max(nums) = 49
high = sum(nums) = 25 + 46 + 28 + 49 + 24 = 172
ans  = infinity


ITERATION 1
low = 49, high = 172
mid = (49 + 172) // 2 = 110        rule: no student reads more than 110 pages

  students = 1, pageCount = 0
  book 25 -> 0  + 25 = 25  <= 110  -> fits, pageCount = 25
  book 46 -> 25 + 46 = 71  <= 110  -> fits, pageCount = 71
  book 28 -> 71 + 28 = 99  <= 110  -> fits, pageCount = 99
  book 49 -> 99 + 49 = 148 >  110  -> full, students = 2, pageCount = 49
  book 24 -> 49 + 24 = 73  <= 110  -> fits, pageCount = 73
  students needed = 2

  2 == 4 ? no, ans stays infinity
  2 >  4 ? no  ->  limit is too generous, move left
  high = mid - 1 = 109


ITERATION 2
low = 49, high = 109
mid = (49 + 109) // 2 = 79         rule: no student reads more than 79 pages

  students = 1, pageCount = 0
  book 25 -> 0  + 25 = 25  <= 79   -> fits, pageCount = 25
  book 46 -> 25 + 46 = 71  <= 79   -> fits, pageCount = 71
  book 28 -> 71 + 28 = 99  >  79   -> full, students = 2, pageCount = 28
  book 49 -> 28 + 49 = 77  <= 79   -> fits, pageCount = 77
  book 24 -> 77 + 24 = 101 >  79   -> full, students = 3, pageCount = 24
  students needed = 3

  3 == 4 ? no, ans stays infinity
  3 >  4 ? no  ->  still too generous, move left
  high = mid - 1 = 78


ITERATION 3
low = 49, high = 78
mid = (49 + 78) // 2 = 63          rule: no student reads more than 63 pages

  students = 1, pageCount = 0
  book 25 -> 0  + 25 = 25  <= 63   -> fits, pageCount = 25
  book 46 -> 25 + 46 = 71  >  63   -> full, students = 2, pageCount = 46
  book 28 -> 46 + 28 = 74  >  63   -> full, students = 3, pageCount = 28
  book 49 -> 28 + 49 = 77  >  63   -> full, students = 4, pageCount = 49
  book 24 -> 49 + 24 = 73  >  63   -> full, students = 5, pageCount = 24
  students needed = 5

  5 == 4 ? no, ans stays infinity
  5 >  4 ? yes ->  limit is too tight, move right
  low = mid + 1 = 64


ITERATION 4
low = 64, high = 78
mid = (64 + 78) // 2 = 71          rule: no student reads more than 71 pages

  students = 1, pageCount = 0
  book 25 -> 0  + 25 = 25  <= 71   -> fits, pageCount = 25
  book 46 -> 25 + 46 = 71  <= 71   -> fits exactly, pageCount = 71
  book 28 -> 71 + 28 = 99  >  71   -> full, students = 2, pageCount = 28
  book 49 -> 28 + 49 = 77  >  71   -> full, students = 3, pageCount = 49
  book 24 -> 49 + 24 = 73  >  71   -> full, students = 4, pageCount = 24
  students needed = 4

  4 == 4 ? yes ->  valid allocation, ans = 71
  4 >  4 ? no  ->  try to squeeze the limit further, move left
  high = mid - 1 = 70

  split found here: 25, 46 | 28 | 49 | 24


ITERATION 5
low = 64, high = 70
mid = (64 + 70) // 2 = 67          rule: no student reads more than 67 pages

  students = 1, pageCount = 0
  book 25 -> 0  + 25 = 25  <= 67   -> fits, pageCount = 25
  book 46 -> 25 + 46 = 71  >  67   -> full, students = 2, pageCount = 46
  book 28 -> 46 + 28 = 74  >  67   -> full, students = 3, pageCount = 28
  book 49 -> 28 + 49 = 77  >  67   -> full, students = 4, pageCount = 49
  book 24 -> 49 + 24 = 73  >  67   -> full, students = 5, pageCount = 24
  students needed = 5

  5 == 4 ? no, ans stays 71
  5 >  4 ? yes ->  too tight, move right
  low = mid + 1 = 68


ITERATION 6
low = 68, high = 70
mid = (68 + 70) // 2 = 69          rule: no student reads more than 69 pages

  students = 1, pageCount = 0
  book 25 -> 0  + 25 = 25  <= 69   -> fits, pageCount = 25
  book 46 -> 25 + 46 = 71  >  69   -> full, students = 2, pageCount = 46
  book 28 -> 46 + 28 = 74  >  69   -> full, students = 3, pageCount = 28
  book 49 -> 28 + 49 = 77  >  69   -> full, students = 4, pageCount = 49
  book 24 -> 49 + 24 = 73  >  69   -> full, students = 5, pageCount = 24
  students needed = 5

  5 == 4 ? no, ans stays 71
  5 >  4 ? yes ->  too tight, move right
  low = mid + 1 = 70


ITERATION 7
low = 70, high = 70
mid = (70 + 70) // 2 = 70          rule: no student reads more than 70 pages

  students = 1, pageCount = 0
  book 25 -> 0  + 25 = 25  <= 70   -> fits, pageCount = 25
  book 46 -> 25 + 46 = 71  >  70   -> full, students = 2, pageCount = 46
  book 28 -> 46 + 28 = 74  >  70   -> full, students = 3, pageCount = 28
  book 49 -> 28 + 49 = 77  >  70   -> full, students = 4, pageCount = 49
  book 24 -> 49 + 24 = 73  >  70   -> full, students = 5, pageCount = 24
  students needed = 5

  5 == 4 ? no, ans stays 71
  5 >  4 ? yes ->  too tight, move right
  low = mid + 1 = 71


LOOP ENDS
low = 71, high = 70  ->  low > high, so the search stops

Return ans = 71
```

<br><br>

## Complexity Analysis

- **Time:** `O(n * log(sum(nums) - max(nums)))`. Each binary search step scans all `n` books once, and the search space shrinks by half every step.
- **Space:** `O(1)`. Only a few counters are used, no extra data structure.

<br><br>

## Edge Case Note

<mark>This version stores the answer only when the student count is exactly equal to m.</mark>

- For almost every input this is fine, because the smallest valid limit usually needs exactly `m` students.
- But when many books have equal or tiny page counts, the greedy count can jump straight from "more than m" to "less than m" without ever landing on `m`.
- Example: `nums = [1, 1, 1, 1]` with `m = 3`. A limit of 1 needs 4 students and a limit of 2 needs 2 students, so no `mid` ever produces exactly 3, and `ans` is returned as infinity even though the real answer is 2.
- Storing the answer whenever `students <= m` (instead of only on equality) keeps the code identical everywhere else and removes this gap.

<br><br>

## Related Problems

- [Split Array Largest Sum (410)](https://leetcode.com/problems/split-array-largest-sum/)
- [Capacity To Ship Packages Within D Days (1011)](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/)
- [Koko Eating Bananas (875)](https://leetcode.com/problems/koko-eating-bananas/)
- [Minimum Number of Days to Make m Bouquets (1482)](https://leetcode.com/problems/minimum-number-of-days-to-make-m-bouquets/)
- [Find the Smallest Divisor Given a Threshold (1283)](https://leetcode.com/problems/find-the-smallest-divisor-given-a-threshold/)
- [Divide Chocolate (1231)](https://leetcode.com/problems/divide-chocolate/)
- [Minimum Limit of Balls in a Bag (1760)](https://leetcode.com/problems/minimum-limit-of-balls-in-a-bag/)
- [Magnetic Force Between Two Balls (1552)](https://leetcode.com/problems/magnetic-force-between-two-balls/)
- [Minimize Max Distance to Gas Station (774)](https://leetcode.com/problems/minimize-max-distance-to-gas-station/)