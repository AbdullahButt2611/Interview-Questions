# "type": "module" in package.json

## Question

What does `"type": "module"` in package.json change?

```json
{
  "type": "module"
}
```

## Answer

<mark>It makes Node treat every .js file in the package as an ES module (ESM) instead of CommonJS. So you use import/export, not require/module.exports.</mark>

- Without the field, the default is `"type": "commonjs"`.

<br><br>

### Syntax Change

```js
// CommonJS (default)
const express = require("express");
module.exports = app;

// ES Module ("type": "module")
import express from "express";
export default app;
```

<br><br>

### What Else Changes

| Feature                   | CommonJS          | ES Module                          |
| :------------------------ | :---------------- | :--------------------------------- |
| Import                    | `require()`       | `import` / `import()`              |
| Export                    | `module.exports`  | `export` / `export default`        |
| `__dirname`, `__filename` | Available         | **Not defined**, use `import.meta` |
| `require`                 | Available         | **Not defined**                    |
| File extension in path    | Optional (`./db`) | **Required** (`./db.js`)           |
| Top-level `await`         | Not allowed       | Allowed                            |
| Strict mode               | Opt-in            | **Always on**                      |
| Loading                   | Sync, at runtime  | Static, resolved before code runs  |

<br><br>

### `__dirname` Fix

```js
// Node 20.11+
const dir = import.meta.dirname;

// Older Node
import { fileURLToPath } from "node:url";
import path from "node:path";
const __dirname = path.dirname(fileURLToPath(import.meta.url));
```

<br><br>

### File Extensions Override It

- `.mjs` is **always** ESM.
- `.cjs` is **always** CommonJS.
- `"type"` only decides how plain `.js` files load.

<br><br>

### Common Errors After Switching

```ini
ReferenceError: require is not defined in ES module scope
ReferenceError: __dirname is not defined in ES module scope
Error [ERR_MODULE_NOT_FOUND]: Cannot find module './db'   (missing .js)
```

<br><br>

### Key Points

- `"type": "module"` = **ESM** for `.js` files, the modern JavaScript standard.
- Same syntax as browsers and front-end code.
- Need an old CommonJS-only API? Use `createRequire(import.meta.url)`.
- The setting applies to the nearest `package.json` folder and below.

<br><br>

## Other Ways to Ask This Question

- What is the difference between CommonJS and ES Modules in Node.js?
- Why is `__dirname` not defined in my Node.js project?
- How do you enable `import` / `export` in Node.js?
- What is the difference between `.mjs` and `.cjs` files?
- Why does Node need the `.js` extension in ESM imports?
- Can you use top-level `await` in Node.js?
