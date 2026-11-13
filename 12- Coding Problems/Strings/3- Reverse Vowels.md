# Reverse Vowels of a String
`LeetCode 75`

### **Problem Statement**

Given a string `s`, reverse only all the vowels in the string and return it.

The vowels are `'a'`, `'e'`, `'i'`, `'o'`, and `'u'`, and they may appear in both lower and upper cases.

**Example 1:**

```text
Input: s = "hello"
Output: "holle"
```

**Example 2:**

```text
Input: s = "leetcode"
Output: "leotcede"
```

**Constraints:**

* `1 <= len(s) <= 3 * 10^5`
* `s` consists of printable ASCII characters.


## Approach 1: Using Stack to Store Vowels (Two-Pass Method)

### **Intuition**

We can first collect all vowels in a separate list (acting as a stack), then make a second pass to replace each vowel in the string with the last one from the stack effectively reversing their order.

### **Algorithm**

1. Iterate over the string and store all vowels in a stack.
2. Convert the string into a list (since strings are immutable in Python).
3. Iterate over the list:

   * If the character is a vowel, replace it with the last vowel popped from the stack.
4. Join the list back into a string and return it.

### **Code Implementation**

```python
class Solution:
    def is_vowel(self, char):
        """Checks if a character is a vowel (case-insensitive)."""
        vowels = "aeiouAEIOU"
        return char in vowels

    def reverseVowels(self, s: str) -> str:
        vowels_stack = []

        # Step 1: Collect all vowels
        for ch in s:
            if self.is_vowel(ch):
                vowels_stack.append(ch)

        # Step 2: Replace vowels in reverse order
        s = list(s)
        for i, ch in enumerate(s):
            if self.is_vowel(ch):
                s[i] = vowels_stack.pop()

        return "".join(s)
```

### **Complexity Analysis**

* **Time Complexity:** O(n) one pass to collect vowels and one to replace them.
* **Space Complexity:** O(n) to store the vowels in the stack.

### **Explanation**

This approach is straightforward and clear but uses additional space proportional to the number of vowels. It’s optimal in time but not space.

## Problem with This Approach

While the time complexity is already optimal (O(n)), the **space usage can be reduced**. The current solution uses an extra list to store vowels. We can instead use two pointers to swap vowels directly in-place.

## Approach 2: Two-Pointer Technique (Optimized In-Place)

### **Intuition**

Use two pointers:

* One starting from the beginning (`left`)
* One from the end (`right`)

Move both pointers inward, and when both point to vowels, swap them.

### **Algorithm**

1. Convert the string to a list for in-place modification.
2. Initialize two pointers: `left = 0`, `right = len(s) - 1`.
3. While `left < right`:

   * If `s[left]` is not a vowel, move `left` forward.
   * If `s[right]` is not a vowel, move `right` backward.
   * Otherwise, swap the two vowels and move both pointers.
4. Join the list and return the result.

### **Code Implementation**

```python
class Solution:
    def reverseVowels(self, s: str) -> str:
        vowels = set("aeiouAEIOU")
        s = list(s)
        left, right = 0, len(s) - 1

        while left < right:
            if s[left] not in vowels:
                left += 1
            elif s[right] not in vowels:
                right -= 1
            else:
                s[left], s[right] = s[right], s[left]
                left += 1
                right -= 1

        return "".join(s)
```

### **Complexity Analysis**

* **Time Complexity:** O(n)
* **Space Complexity:** O(1) — only uses pointers and a small set of vowels.

### **Explanation**

This method achieves the same time complexity as before but uses constant space, making it more efficient. It processes the string in a single pass using the two-pointer technique.

## Summary Comparison

| Approach           | Description                             | Time | Space | Remarks                              |
| ------------------ | --------------------------------------- | ---- | ----- | ------------------------------------ |
| **1. Stack-Based** | Collect vowels, then replace in reverse | O(n) | O(n)  | Easy to understand, uses extra space |
| **2. Two-Pointer** | Swap vowels in-place using two pointers | O(n) | O(1)  | Most efficient and clean solution  |
