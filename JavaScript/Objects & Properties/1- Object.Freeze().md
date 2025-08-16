## What is the use of Object.freeze() in JavaScript
`Turing - JavaScript`

---

**`Object.freeze()` in JavaScript is used to make an object immutable, meaning you cannot add, remove, or modify its properties and values. Once an object is frozen, it becomes read-only and cannot be changed in any way.**

Example:

```js
const user = { name: "Ali" };
Object.freeze(user);

user.name = "Ahmed";  // ❌ change not allowed
user.age = 25;        // ❌ new property not allowed

console.log(user); // { name: "Ali" }
```