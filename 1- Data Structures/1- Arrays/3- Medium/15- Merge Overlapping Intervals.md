# Merge Intervals

`Google` • `Meta` • `Amazon` • `Apple` • `Netflix` • `Microsoft` • `Palantir` • `Patreon` • `Rivian`
<br>

## Problem Statement

Given an array of intervals where `intervals[i] = [starti, endi]`, merge all overlapping intervals and return an array of the non-overlapping intervals that cover all the intervals in the input.

**Examples**

**Example 1:**
```
Input:  intervals = [[1,3],[2,6],[8,10],[15,18]]
Output: [[1,6],[8,10],[15,18]]
```
Explanation: Intervals `[1,3]` and `[2,6]` overlap, so they merge into `[1,6]`.

**Example 2:**
```
Input:  intervals = [[1,4],[4,5]]
Output: [[1,5]]
```
Explanation: Intervals `[1,4]` and `[4,5]` touch at endpoint `4`, so they are considered overlapping.

**Example 3:**
```
Input:  intervals = [[4,7],[1,4]]
Output: [[1,7]]
```
Explanation: Intervals are unsorted. After sorting, `[1,4]` and `[4,7]` overlap and merge into `[1,7]`.

**Constraints**
- `1 <= intervals.length <= 10^4`
- `intervals[i].length == 2`
- `0 <= starti <= endi <= 10^4`

<br><br>

## Approach: Sort + Linear Scan (Optimal)

**Intuition**

The key insight is that if we sort the intervals by their start time, any overlapping intervals are guaranteed to be adjacent to each other. This means we never need to compare a current interval against intervals far to the left. A single left-to-right pass is sufficient.

After sorting:
- If the current interval's start is greater than the last merged interval's end, there is no overlap. Add the current interval as a new entry.
- Otherwise, the intervals overlap. Extend the end of the last merged interval to the maximum of both ends.

**Visual Walkthrough**

```
Input: [[1,3],[2,6],[8,10],[15,18]]

After sorting: [[1,3],[2,6],[8,10],[15,18]]  (already sorted)

Step 1: result = []        -> Append [1,3]         -> result = [[1,3]]
Step 2: interval = [2,6]   -> 2 <= 3 (overlap)     -> extend: result = [[1,6]]
Step 3: interval = [8,10]  -> 8 > 6  (no overlap)  -> append: result = [[1,6],[8,10]]
Step 4: interval = [15,18] -> 15 > 10 (no overlap) -> append: result = [[1,6],[8,10],[15,18]]

Output: [[1,6],[8,10],[15,18]]
```

**Approach**

1. Sort intervals by start time.
2. Initialize an empty result list.
3. For each interval, compare it against the last interval in result:
   - No overlap: append the interval directly.
   - Overlap: update the end of the last interval to `max(last_end, current_end)`.
4. Return result.

```python
class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        # Sort intervals by start time so overlapping intervals become adjacent
        intervals.sort()

        merged = []
        last = -1  # Index of the last interval added to merged

        for start, end in intervals:
            if not merged or start > merged[last][1]:
                # No overlap: current interval starts after the last merged one ends
                merged.append([start, end])
                last += 1
            else:
                # Overlap: extend the end of the last merged interval if needed
                # Use max to handle containment e.g. [1,10] containing [2,5]
                merged[last][1] = max(end, merged[last][1])

        return merged
```

**Why `max` on the end?**

A contained interval like `[1,10]` followed by `[2,5]` would incorrectly shrink the end to `5` without the `max`. Always take the larger of the two ends to handle containment correctly.

**Complexity Analysis**

| | |
|---|---|
| Time Complexity | O(n log n) dominated by the sort; the scan is O(n) |
| Space Complexity | O(n) for the output list (O(log n) additional for sort stack) |

**Why this is optimal**

Sorting is unavoidable here because the input can be in any order. After sorting, one linear pass is all we need, making this O(n log n) overall. No comparison-based approach can do better than O(n log n) on unsorted data.

<br><br>

## Summary

| | |
|---|---|
| Time Complexity | O(n log n) |
| Space Complexity | O(n) |

<br><br>

## Edge Cases to Consider

- **Single interval:** `[[5,10]]` returns `[[5,10]]` with no merges needed.
- **All intervals overlap:** `[[1,4],[2,5],[3,6]]` merges into `[[1,6]]`.
- **Touching endpoints:** `[[1,4],[4,5]]` should merge into `[[1,5]]` since `4 <= 4`.
- **Contained intervals:** `[[1,10],[2,5]]` should return `[[1,10]]`, not `[[1,5]]`. This is why we use `max` on the end.
- **Already non-overlapping:** `[[1,2],[3,4],[5,6]]` returns the same list unchanged.
- **Unsorted input:** `[[4,7],[1,4]]` must be sorted first before processing.

<br><br>

## Related Problems

- **[Insert Interval (LeetCode 57)](https://leetcode.com/problems/insert-interval/):** Insert a new interval into a sorted list of non-overlapping intervals and merge if necessary.
- **[Meeting Rooms II (LeetCode 253)](https://leetcode.com/problems/meeting-rooms-ii/):** Find the minimum number of meeting rooms required given a list of meeting time intervals.
- **[Interval List Intersections (LeetCode 986)](https://leetcode.com/problems/interval-list-intersections/):** Find all intersecting intervals between two sorted interval lists.
- **[Non-overlapping Intervals (LeetCode 435)](https://leetcode.com/problems/non-overlapping-intervals/):** Find the minimum number of intervals to remove to make the rest non-overlapping.
- **[Minimum Number of Arrows to Burst Balloons (LeetCode 452)](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/):** Classic greedy interval problem using similar sorting and overlap logic.
- **[Employee Free Time (LeetCode 759)](https://leetcode.com/problems/employee-free-time/):** Find the common free time across all employees' schedules using interval merging.