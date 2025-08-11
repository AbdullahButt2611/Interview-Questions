## Greatest Common Divisor of Strings
`Leetcode 75`

For two strings s and t, we say "t divides s" if and only if s = t + t + t + ... + t + t (i.e., t is concatenated with itself one or more times).

Given two strings str1 and str2, return the largest string x such that x divides both str1 and str2.

#### Example 1:
Input: str1 = "ABCABC", str2 = "ABC"
Output: "ABC"

#### Example 2:
Input: str1 = "ABABAB", str2 = "ABAB"
Output: "AB"

#### Example 3:
Input: str1 = "LEET", str2 = "CODE"
Output: ""

----

### Brute Force Solution

The number of characters in the divisor will be equal to the GCD of lengths of both the strings. Once you found that next step is that take tat number of characters from the string and start repeating it equal to the `len(string)//len(gcd)` times. And when you repeat it should make the same strings if not then thats not the GCD.

```
class Solution:

    def gcd_recursively(self, a, b) -> int:
        a ,b = abs(a), abs(b)
        if b == 0:
            return a
        
        return self.gcd_recursively(b, a % b)

    def gcdOfStrings(self, str1: str, str2: str) -> str:
        len_gcd = 0

        str1_len = len(str1)
        str2_len = len(str2)

        if str1_len > str2_len:
            len_gcd = self.gcd_recursively(str1_len, str2_len)
        else:
            len_gcd = self.gcd_recursively(str2_len, str1_len)
        
        candidate_string = str1[:len_gcd] 
        matching_string = ""
        for i in range(0, str1_len//len_gcd):
            matching_string += candidate_string

        if str1 != matching_string:
            return ""

        matching_string = ""
        for i in range(0, str2_len//len_gcd):
            matching_string += candidate_string
            
        if str2 != matching_string:
            return ""

        return candidate_string 
```

#### Points to Ponder

1. ##### Repetition check could be cleaner:
    You manually build the matching_string with loops; Python's string multiplication can make it simpler. \
2. ##### Unnecessary length comparison: 
    GCD is symmetric, so no need to check if str1_len > str2_len.
3. ##### Division check shortcut: 
    Before doing GCD, you can check if str1 + str2 == str2 + str1 — if not, return "" immediately (because they must share a common pattern to have a divisor).
4. ##### Avoid extra string concatenations: 
    String building in a loop can be slow; use "pattern" * count.

----

### Optimized Solution Using GCD

```
class Solution:
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        from math import gcd
        
        # Quick check: if concatenations differ, no common pattern exists
        if str1 + str2 != str2 + str1:
            return ""
        
        # GCD of the lengths gives the largest possible common divisor length
        length_gcd = gcd(len(str1), len(str2))
        return str1[:length_gcd]
```

#### Why this works:

1. If str1 + str2 != str2 + str1, then they cannot share a common divisor string (mathematical property of periodic strings).
2. Otherwise, the largest divisor must have length = gcd(len(str1), len(str2)).

#### Complexity:
- Time: O(n) (only one pass to verify + substring slicing).
- Space: O(1).

