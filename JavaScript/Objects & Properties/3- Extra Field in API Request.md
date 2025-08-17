## Removing extra object fields before sending API request in JavaScript

You are working on an enterprise project for a bank. You have been assigned to the Customer Account module that deals with managing the bank accounts of customers. The API contract to send customer details allows fields such as accountNumber, customerId, currentBalance, addressLine1, addressLine2, and contactNumber. However, in the frontend, while you were creating the request body you encountered an additional key which is important to maintain the state on the frontend. You need to make a decision to identify the best way to remove the extra field by replacing ?? to create a request body for the API.

```js
let bankAccount = {
    accountNumber: "A458962361",
    customerId: "A1056932036",
    currentBalance: "5896036",
    isSelected: true,
    addressLine1: "Parkway Avenue",
    addressLine2: "United States",
    contactNumber: 90112569145,
};

function sendToApi() {
    fetch("http://example.com/").then((response) => response.json()).then((data) => console.log(data));
} ?? sendToApi(newObj);
```

`Turing - JavaScript`

---

Here the issue is that `bankAccount` contains an **extra frontend-only property** `isSelected`, which **must not** be sent to the backend API.

The cleanest and most maintainable way to remove it is to use **object destructuring with rest properties**.

### Solution

```javascript
const { isSelected, ...newObj } = bankAccount;
```

### Full example

```javascript
let bankAccount = {
  accountNumber: "A458962361",
  customerId: "A1056932036",
  currentBalance: "5896036",
  isSelected: true, // frontend-only field
  addressLine1: "Parkway Avenue",
  addressLine2: "United States",
  contactNumber: 90112569145,
};

function sendToApi(obj) {
  fetch("http://example.com/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(obj),
  })
    .then((response) => response.json())
    .then((data) => console.log(data));
}

// ✅ Remove isSelected without mutating original
const { isSelected, ...newObj } = bankAccount;

sendToApi(newObj);
```

### Why this is best

* **Immutable**: doesn’t modify `bankAccount`.
* **Scalable**: easy to add/remove more frontend-only keys later.
* **Readable**: instantly clear which key is excluded.