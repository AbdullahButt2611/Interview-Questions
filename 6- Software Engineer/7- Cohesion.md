## What is cohesion? Explain with an example and code
`Technosoft`
<br><br>

Cohesion in software engineering refers to the degree to which the elements within a module or class work together to fulfill a single, well-defined purpose. High cohesion implies that the components of a module are closely related and focused on a specific task, which enhances maintainability, readability, and reusability of the code. Conversely, low cohesion indicates that a module contains elements that serve multiple unrelated purposes, making it harder to understand and maintain.

## Types of Cohesion
Cohesion can be categorized into several types, from worst to best:
- **Coincidental Cohesion**: Elements are grouped arbitrarily with no meaningful relationship (e.g., a utility class with unrelated functions).
- **Logical Cohesion**: Elements are grouped because they perform similar functions but are different in nature (e.g., handling various user inputs).
- **Temporal Cohesion**: Elements are related by their timing in execution (e.g., initialization routines).
- **Procedural Cohesion**: Elements are grouped because they follow a specific sequence of execution (e.g., steps in a process).
- **Communicational Cohesion**: Elements operate on the same data or contribute to the same output (e.g., updating and printing user records).
- **Sequential Cohesion**: The output of one element serves as input to another (e.g., processing data in stages).
- **Functional Cohesion**: All elements contribute to a single well-defined task (e.g., a module that handles all aspects of user authentication) and is the most desirable type of cohesion

## Example of High Cohesion
Consider a class designed for user authentication:

```python
class UserAuthentication:
    def login(self, username, password):
        # Logic for user login
        pass

    def logout(self):
        # Logic for user logout
        pass

    def reset_password(self, email):
        # Logic for password reset
        pass
```

In this example, all methods within the `UserAuthentication` class are focused on user authentication tasks, demonstrating high cohesion. Each method is related to the primary responsibility of managing user access, making it easier to understand and maintain.

## Example of Low Cohesion
Now consider a poorly designed class:

```python
class Utility:
    def login(self, username, password):
        # Logic for user login
        pass

    def calculate_average(self, numbers):
        # Logic for calculating average
        return sum(numbers) / len(numbers)

    def send_email(self, recipient, message):
        # Logic for sending an email
        pass
```

Here, the `Utility` class combines unrelated functionalities: user authentication, statistical calculations, and email sending. This low cohesion makes it difficult to understand the purpose of the class and complicates maintenance efforts.
In summary, achieving high cohesion in software design is crucial for developing clear and maintainable code structures. It allows developers to create modules that have focused responsibilities, thereby enhancing overall software quality.