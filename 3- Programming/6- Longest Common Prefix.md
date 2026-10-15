# Longest common prefix (from list of strings)
`Educative`

```python
def longest_common_prefix(strs):
    result = ""
    
    # Sort the array of strings
    strs.sort()
    
    # Get the first and last strings
    first = list(strs[0])
    last = list(strs[-1])
    
    # Start comparing characters
    for i in range(len(first)):
        if first[i] != last[i]:
            break
        result += first[i]
    
    return result

# Example usage:
strings = ["flower", "flow", "flight"]
print(longest_common_prefix(strings))  # Output: "fl"
```

This Python function longest_common_prefix takes a list of strings strs as input and returns the longest common prefix among them. Firstly, the function initializes an empty string result to store the common prefix. Then, it sorts the list of strings alphabetically using Python's sort method. By doing this, the function ensures that the common prefix can be found by comparing the first and last strings in the sorted list. It converts both the first and last strings to character arrays using Python's list function. After that, the function iterates through the characters of the first string, comparing each character with the corresponding character in the last string. If a mismatch is found, the loop breaks, indicating the end of the common prefix. Otherwise, it appends the matching characters to the result string. Finally, the function returns the result, which contains the longest common prefix found among the input strings.

## Better code

```python
def longest_common_prefix(strs):
    if not strs:
        return ""
    
    # Start with the first string as the prefix
    prefix = strs[0]
    
    # Compare the prefix with each string in the list
    for string in strs[1:]:
        # Reduce the prefix as long as it matches the beginning of the string
        while not string.startswith(prefix):
            print(string, prefix)
            prefix = prefix[:-1]
            if not prefix:
                return ""
    
    return prefix

# Example usage:
strings = ["flower", "flow", "flight"]
print(longest_common_prefix(strings))  # Output: "fl"
```