## Explain coupling along with a coding example
`Technosoft`
<br><br>

In software engineering, **coupling** refers to the level of dependency between different modules or components of a system. A high level of coupling means that changes in one module may impact others, making the system less flexible and harder to maintain. Low coupling, on the other hand, implies that modules are more independent, making the system more modular and easier to modify or extend.

### Types of Coupling
1. **Tight (High) Coupling**: Modules are heavily dependent on each other, which can make code more complex and difficult to reuse.
2. **Loose (Low) Coupling**: Modules interact with each other through well-defined interfaces, minimizing dependencies. This approach improves flexibility and maintainability.
<br><br>

### Example of Tight vs. Loose Coupling

#### Tight Coupling Example
In this example, class `Order` depends directly on the `Customer` class. Any change in `Customer` could affect `Order`.
```python
class Customer:
    def __init__(self, name):
        self.name = name

class Order:
    def __init__(self, customer):
        # Direct dependency on Customer class
        self.customer = customer
        print(f"Order placed by {self.customer.name}")

# Usage
customer = Customer("Alice")
order = Order(customer)
```
In this code, Order directly accesses the Customer object. If Customer changes, Order might also need updates, creating a tightly coupled relationship.

#### Loose Coupling Example
By introducing an interface or abstraction, we can make the coupling looser. Here, `Order` uses a `CustomerInterface` instead of the concrete `Customer` class.

```python
class CustomerInterface:
    def get_customer_name(self):
        raise NotImplementedError

class Customer(CustomerInterface):
    def __init__(self, name):
        self.name = name

    def get_customer_name(self):
        return self.name

class Order:
    def __init__(self, customer: CustomerInterface):
        # Uses interface instead of concrete class
        self.customer = customer
        print(f"Order placed by {self.customer.get_customer_name()}")

# Usage
customer = Customer("Alice")
order = Order(customer)
```

In this version, Order depends only on CustomerInterface, making it easier to replace or modify the Customer class without affecting Order. This reduces dependencies, achieving loose coupling.