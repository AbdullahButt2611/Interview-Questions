## What is Code Encryption in JavaScript?

**Code Encryption is the process of transforming source code into an unreadable or encoded format using cryptographic techniques, so that only authorized users or systems can decrypt and execute it.** It is mainly used to **protect sensitive logic, prevent theft, and secure applications from reverse engineering.**

### **Example**

Original code:

```js
console.log("Hello World");
```

Encrypted (example in Base64 encoding, not real execution-ready encryption):

```
Y29uc29sZS5sb2coIkhlbGxvIFdvcmxkIik7
```

This encrypted string can be stored or transmitted, and only after **decryption** will it become executable again.

✅ **Purpose:**

* Protect intellectual property
* Prevent unauthorized access
* Enhance application security