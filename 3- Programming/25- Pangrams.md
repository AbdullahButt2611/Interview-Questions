### A pangram is a string that contains every letter of the alphabet. Given a sentence determine whether it is a pangram in the English alphabet. Ignore case. Return either pangram or not pangram as appropriate.

`HackerRank`
<br><br>

## Solution

```python
def pangrams(s):
    alphabets_set = set()
    s = s.lower()
    
    for alphabet in s:
        if not alphabet == " ":
            alphabets_set.add(alphabet)
    
    if len(alphabets_set) == 26:
        return 'pangram'
    else:
        return 'not pangram'
```
<br>

---------------
<h3 align="center">OR</h3>

---------------
<br>

```python
def is_pangram(sentence):
    sentence = sentence.lower()
    
    alphabet_set = set("abcdefghijklmnopqrstuvwxyz")

    sentence_set = set(filter(str.isalpha, sentence))
    
    if alphabet_set.issubset(sentence_set):
        return "pangram"
    else:
        return "not pangram"
```