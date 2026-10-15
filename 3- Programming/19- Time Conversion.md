### Given a time in 12-hour AM/PM format, convert it to military (24-hour) time.Note: - 12:00:00AM on a 12-hour clock is 00:00:00 on a 24-hour clock. 12:00:00PM on a 12-hour clock is 12:00:00 on a 24-hour clock. 
`HackerRank`

#### Function Description
> Complete the timeConversion function in the editor below. It should return a new string representing the input time in 24 hour format.timeConversion has the following parameter(s):

> string s: a time in  hour format


### Sample Input
```
07:05:45PM
```


### Sample Output
```
19:05:45
```


### Code

```python

import datetime

def timeConversion(s):
    if s[-2:] == 'AM' and s[:2] == '12':
        return "00" + s[2:-2]
    
    elif s[-2:] == 'AM':
        return s[:-2]
        
    elif s[-2:] == 'PM' and s[:2] == '12':
        return s[:-2]
        
    else:
        return str((int(s[:2])+12))+s[2:-2]

```