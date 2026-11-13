`Arbisoft`

# Question
You are tasked with developing a Python API that needs to be both efficient and robust against excessive usage. To achieve this, you must implement rate limiting on an API endpoint. Additionally, the API will provide a feature where users can retrieve the next available ending of a story from a given list of story segments.
### 1. Rate Limiting:
- Implement a Python decorator that enforces rate limiting on the API endpoint. The decorator should allow a specified number of API calls per user within a given time period. If the rate limit is exceeded, the API should return an appropriate message indicating that the user has exceeded the allowed number of requests and inform them when they can make the next request.
### 2. Story Ending Retrieval:
- Create an API function that uses the rate limiting decorator and returns the next available ending of a story from a provided list of story segments. Each time the API is called, it should return the next item from the list. If there are no more endings available, the API should return a message indicating that no more story endings are available.
### Tasks:
- Write the Python decorator for rate limiting.
- Implement the API function to retrieve the next story ending from a list.
- Demonstrate how the rate limiting decorator can be applied to the API function.
### Example:
Given a list of story endings: `["Ending 1", "Ending 2", "Ending 3"]`, the API should return "Ending 1" on the first call, "Ending 2" on the second call, and so on. If the API is called more than the allowed number of times within the rate limit period, it should return a rate limit exceeded message.
<br><br><br>

# Solution

### Rate Limiting Decorator
Here's how you can write a decorator in Python to apply rate limiting on an API:

```python
import time
from functools import wraps

# This will store the API call timestamps per user
rate_limit_cache = {}

def rate_limit(max_calls: int, period: int):
    """
    A decorator to apply rate limiting to an API endpoint.
    
    :param max_calls: Maximum number of allowed calls within the period.
    :param period: Time window in seconds for the rate limit.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(user_id, *args, **kwargs):
            current_time = time.time()
            if user_id not in rate_limit_cache:
                rate_limit_cache[user_id] = []

            # Remove outdated calls
            rate_limit_cache[user_id] = [timestamp for timestamp in rate_limit_cache[user_id] 
                                         if current_time - timestamp < period]

            # Check if rate limit is exceeded
            if len(rate_limit_cache[user_id]) >= max_calls:
                return f"Rate limit exceeded. Try again in {int(period - (current_time - rate_limit_cache[user_id][0]))} seconds."

            # Log the call
            rate_limit_cache[user_id].append(current_time)

            return func(user_id, *args, **kwargs)
        return wrapper
    return decorator
```

### Usage of the Rate Limiting Decorator
You can apply this decorator to an API function. Let's assume we have an API function that provides the next ending of a storybook:

```python
@rate_limit(max_calls=5, period=60)  # Allows 5 calls per minute
def get_next_story_ending(user_id, story_list):
    # Here, we'll assume the next ending is simply the next item in the list
    return story_list.pop(0) if story_list else "No more story endings available."

# Example usage:
user_id = "user_123"
story_list = ["Ending 1", "Ending 2", "Ending 3"]

print(get_next_story_ending(user_id, story_list))  # Should print "Ending 1"
print(get_next_story_ending(user_id, story_list))  # Should print "Ending 2"
```
<br><br><br>

# Explanation of the Solution
- #### Decorator Function (rate_limit):
    - The rate_limit decorator is designed to control the number of API calls per user within a given time frame.
    - The decorator uses a cache (dictionary) to track the timestamps of each user's API calls.
    - It removes outdated timestamps (those outside the time window) and checks if the number of remaining timestamps exceeds the allowed maximum calls.
    - If the limit is exceeded, it returns a message to the user indicating when they can try again.
    - Otherwise, it logs the current call and proceeds to execute the API function.

- #### API Function (get_next_story_ending):
    - This function simulates fetching the next ending of a storybook from a list.
    - The rate_limit decorator ensures that the function is not called too frequently by the same user, thus protecting the API from abuse.