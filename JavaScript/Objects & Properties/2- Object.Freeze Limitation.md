## Limitations of Object.freeze() in JavaScript

You are the backend developer for an enterprise bank project. Within this, you are assigned the task to sort the bank accounts by their balances. However, during the program execution flow you want to ensure that the code does not modify the customer details. You tried Object.freeze but it is not throwing an error when a developer is modifying the bank account details such as balance. What is missing here?

```
const bankAccount = [{
    customerId: "A10120123",
    accountNumber: "502362145",
    balance: 5000,
    addressLine1: "Parkway Avenue",
    addressLine2: "United States",
}, {
    customerId: "A101201231",
    accountNumber: "5023621451",
    balance: 10000,
    addressLine1: "CA Avenue",
    addressLine2: "United States",
}, ];
for (let index = 0; index < bankAccount.length; index++) {
    Object.freeze(bankAccount[index]);
}
bankAccount[1].balance = 200;
console.log(bankAccount[1].balance);
```

`Turing - JavaScript`

---

In current code, the missing piece is **`use strict` mode**.

### Why it's happening

* `Object.freeze()` **does** prevent modifications to properties, but in **non-strict mode**, JavaScript fails **silently** when you try to change a frozen object.
* Without `use strict`, if you do:

  ```javascript
  frozenObj.prop = 'new value';
  ```

  JavaScript will just ignore it, no error thrown.
* In **strict mode**, trying to modify a frozen object's property will throw a **`TypeError`**.


### Fixed code

```javascript
"use strict"; // This is what you’re missing

const bankAccount = [
  {
    customerId: "A10120123",
    accountNumber: "502362145",
    balance: 5000,
    addressLine1: "Parkway Avenue",
    addressLine2: "United States",
  },
  {
    customerId: "A101201231",
    accountNumber: "5023621451",
    balance: 10000,
    addressLine1: "CA Avenue",
    addressLine2: "United States",
  },
];

for (let index = 0; index < bankAccount.length; index++) {
  Object.freeze(bankAccount[index]);
}

bankAccount[1].balance = 200; // ❌ TypeError in strict mode

console.log(bankAccount[1].balance);
```

### Key takeaway

> `Object.freeze()` prevents changes, but **strict mode** is required if you want JavaScript to actually **throw an error** when a modification is attempted.

