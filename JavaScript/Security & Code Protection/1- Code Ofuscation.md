## What is Code Obfuscation in JavaScript?

**Code Obfuscation is the process of deliberately making source code difficult to read or understand while keeping its functionality the same.** It is mainly used to protect code from **reverse engineering, tampering, or unauthorized copying.**

### **Example**

Original code (readable):

```js
function add(a, b) {
  return a + b;
}
```

Obfuscated code (hard to read):

```js
function _0x12a(_0x1a,_0x2b){return _0x1a+_0x2b;}
```

Both do the **same thing**, but the second one is much harder to understand.

✅ **Purpose:**

* Protect intellectual property
* Increase security against code theft
* Prevent easy reverse engineering