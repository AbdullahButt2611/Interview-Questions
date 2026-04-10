# Minimum Distance Between Three Equal Elements I

## Problem Statement

You are given an integer array `nums`.

A tuple `(i, j, k)` of three **distinct indices** is called **good** if:

```text
nums[i] == nums[j] == nums[k]
```

The **distance** of a good tuple is defined as:

```text
|i - j| + |j - k| + |k - i|
```

Return the **minimum possible distance** of any good tuple. If no such tuple exists, return `-1`.

## Examples

### Example 1

```text
Input: nums = [1,2,1,1,3]
Output: 6
```

**Explanation**: Indices `(2,3,0)` give distance `|2-3| + |3-0| + |0-2| = 1 + 3 + 2 = 6`.

### Example 2

```text
Input: nums = [1,1,2,3,2,1,2]
Output: 8
```

### Example 3

```text
Input: nums = [1]
Output: -1
```

## Constraints

- `1 <= nums.length <= 100`
- `1 <= nums[i] <= nums.length`

## Approach 1: Brute Force (Educational)

### Step-by-Step Explanation

Let's first understand the problem completely with brute force:

```python
class Solution:
    def minimumDistance(self, nums):
        n = len(nums)
        min_dist = float('inf')

        # Check every possible triplet of distinct indices
        for i in range(n):
            for j in range(i + 1, n):  # j > i ensures no duplicates
                for k in range(j + 1, n):  # k > j ensures i < j < k
                    # Only process if all three values are equal
                    if nums[i] == nums[j] == nums[k]:
                        # Calculate actual distance formula
                        dist = abs(i - j) + abs(j - k) + abs(k - i)
                        min_dist = min(min_dist, dist)

        return -1 if min_dist == float('inf') else min_dist
```

**Time Complexity**: O(n³) - too slow for larger arrays.

## Approach 2: Mathematical Simplification (Optimal)

### Step 1: Key Mathematical Insight

**Why does the distance simplify to `2 * (k - i)`?**

Since we can always choose indices where `i < j < k` (we're just looking for minimum distance, order doesn't matter), let's expand the formula:

```
|i - j| = j - i    (because j > i)
|j - k| = k - j    (because k > j)  
|k - i| = k - i    (because k > i)
```

Now add them up:

```
Distance = (j - i) + (k - j) + (k - i)
         = j - i + k - j + k - i    # j and -j cancel out
         = 2k - 2i
         = 2 * (k - i)
```

**The `j` completely disappears!** The middle index doesn't affect the distance at all.

**Example verification**:
- For indices `[0, 2, 3]` (from Example 1):
- `2 * (3 - 0) = 2 * 3 = 6` ✓ Matches brute force result.

### Step 2: What affects the minimum distance?

Since distance = `2 * (k - i)`:
- `2` is constant
- We need to **minimize `(k - i)`**
- `(k - i)` is the **distance between first and last index of any 3 equal elements**

### Step 3: Strategy

1. **Group indices by value**: Store all positions where each number appears
2. **For each number appearing ≥3 times**: Find the **closest** 3 occurrences
3. **Why closest 3?** Because they give the smallest `(k - i)`
4. **How to find closest 3?** Check consecutive triplets in the sorted index list

### Step-by-Step Code Walkthrough

```python
from collections import defaultdict

class Solution:
    def minimumDistance(self, nums):
        # Step 1: Group indices by their values
        # Example: nums = [1,2,1,1,3] -> {1: [0,2,3], 2: [1], 3: [4]}
        num_indices = defaultdict(list)
        for idx, num in enumerate(nums):
            num_indices[num].append(idx)
        
        min_dist = float('inf')
        
        # Step 2: Check each number's indices
        for indices in num_indices.values():
            # Skip if less than 3 occurrences
            if len(indices) < 3:
                continue
            
            # indices are naturally sorted since we added in order
            # Example for 1: [0,2,3]
            
            # Step 3: Check every consecutive triplet
            # We only need first (i) and last (k) of each triplet
            for x in range(len(indices) - 2):  # x+2 must exist
                i = indices[x]        # First index of triplet
                k = indices[x + 2]    # Third index of triplet
                # j = indices[x + 1] is never needed!
                
                distance = 2 * (k - i)
                min_dist = min(min_dist, distance)
        
        return -1 if min_dist == float('inf') else min_dist
```

**Trace Example 1**: `nums = [1,2,1,1,3]`
- `num_indices[1] = [0,2,3]`
- Triplet `[0,2,3]`: `2 * (3 - 0) = 6`
- Result: `6`

## Complexity Analysis

**Time**: O(n)
- Building `num_indices`: O(n)
- For each number, checking triplets: O(count) where total counts sum to n

**Space**: O(n) for storing indices

## Why This Works (Summary)

| What We Learned | Why It Matters |
|-----------------|---------------|
| Distance = `2*(k-i)` | Middle index `j` is irrelevant |
| Minimize `(k-i)` | Pick closest 3 occurrences |
| Consecutive triplets | Guaranteed to find minimum span |
| Grouping by value | Only same values can form good tuples |

## Edge Cases Explained

1. **No number appears 3+ times**: `min_dist` stays `inf` → return `-1`
2. **Exactly 3 occurrences**: One triplet to check
3. **Many occurrences**: Multiple overlapping triplets, we take minimum
4. **Array length < 3**: Automatically handled by index grouping

## Key Takeaways for Interviews

1. **Always simplify math first** - look for cancellations like `j - j = 0`
2. **Understand what REALLY affects the answer** - here only `k-i` matters
3. **Group by value** when same elements are required
4. **Consecutive groups often give minimum distance**
5. **Brute force → Math insight → Optimal** is a common interview pattern