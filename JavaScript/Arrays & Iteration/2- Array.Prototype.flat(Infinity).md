## What is Array.prototype.flat(Infinity) and its purpose in JavaScript?

---

**`Array.prototype.flat(Infinity)` is a JavaScript method used to recursively flatten a nested array to any depth. The purpose is to convert multi-dimensional arrays into a single-level array.**

Example:

```js
const arr = [1, [2, [3, [4]]]];
console.log(arr.flat(Infinity)); 
// Output: [1, 2, 3, 4]
```