# Python Packages

`Accenture` • `TCS` • `Infosys` • `Cognizant` • `Capgemini` • `Wipro`

## Question

What is a Python package?

- How is it different from a module?
- What makes a folder count as a package?

<br><br>

## Answer

### In One Line

A package is a folder that groups several related Python files (modules) together under one name.

<br><br>

### Module vs Package

- A **module** is a single `.py` file (for example, `utils.py`).
- A **package** is a folder that holds many modules together.
- A **sub-package** is just a package placed inside another package.

Easy way to picture it:

- Module = one page.
- Package = a folder full of pages.
- Sub-package = a smaller folder inside that folder.

The big win is the dotted name. Instead of a messy pile of loose files, you get a clean hierarchy like `shop.payments.card`.

<br><br>

### What a Package Looks Like

```ini
shop/
    __init__.py
    products.py
    payments/
        __init__.py
        card.py
```

Here is what each part means:

- `shop` is a package (a folder with an `__init__.py`).
- `products.py` is a module inside it.
- `payments` is a sub-package (a package inside a package).
- `card.py` is a module inside the sub-package.

<br><br>

### The `__init__.py` File

This small file is what traditionally turns a plain folder into a package.

- It marks the folder as a package.
- It runs automatically the first time the package is imported, so it is a good spot for setup code.
- It can be completely empty, which is very common and perfectly fine.
- It can also expose a clean API (for example, pulling important names up so users can write `from shop import checkout` instead of a long path).

<br><br>

### How You Import From a Package

Once the structure above exists, you reach inside it using dotted names:

```python
import shop.products
from shop.payments.card import pay

shop.products.list_all()
pay(amount=100)
```

Python walks the path one level at a time. It finds `shop`, then `shop.payments`, then `shop.payments.card`.

<br><br>

### Regular vs Namespace Packages

There are two flavors, and you will almost always use the first one.

- **Regular package**: has an `__init__.py` and lives in one folder. This is the normal, everyday case.
- **Namespace package**: has no `__init__.py`, and can be split across several folders that Python merges into one name. This is the special case for spreading one package across different locations.

Simple rule: add an `__init__.py` and you get a regular package. Leave it out only when you specifically need the split behavior.

<br><br>

### Quick Recap

- Module = one file, package = a folder of modules, sub-package = a folder inside a folder.
- `__init__.py` traditionally marks a folder as a package and is allowed to be empty.
- Dotted names (`shop.payments.card`) let you reach neatly into the hierarchy.

<mark>A package is simply a folder of related modules that Python can import as one unit using dotted names.</mark>

<br><br>

## Related Questions

- What is the difference between a module and a package in Python?
- What is the purpose of the `__init__.py` file?
- What is a namespace package, and how does it differ from a regular package?
- How does Python find a package when you import it?
- How do you create and install your own Python package with pip?
- What does `from package import *` do, and how does `__all__` control it?