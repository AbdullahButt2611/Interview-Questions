# express.json() Middleware

## Question

What does `express.json()` do?

```js
app.use(express.json());
```

## Answer

<mark>It is built-in middleware that reads the request body, parses it as JSON when Content-Type is application/json, and puts the result on req.body. Without it, req.body is undefined.</mark>

<br><br>

### Without vs With

```js
app.post("/users", (req, res) => {
  res.json(req.body);
});
```

```ini
POST /users   Content-Type: application/json   {"name":"Ali"}

Without express.json():  req.body = undefined
With express.json():     req.body = { name: "Ali" }
```

- Node delivers the body as a **stream of bytes**. Express does not read it on its own.
- Register it **before** the routes that need `req.body`.

<br><br>

### What It Checks

| Situation                                           | Result                                     |
| :-------------------------------------------------- | :----------------------------------------- |
| `Content-Type: application/json`, valid             | Parsed into `req.body`                     |
| Wrong or missing `Content-Type`                     | Skipped, `req.body` stays `undefined`      |
| Invalid JSON (`{"name":}`)                          | **400** error (`entity.parse.failed`)      |
| Body larger than `limit` (default 100kb)            | **413** Payload Too Large                  |
| Top-level primitive (`"hello"`) with `strict: true` | **400** error, only objects/arrays allowed |

<br><br>

### Useful Options

```js
app.use(express.json({
  limit: "1mb",              // max body size (default "100kb")
  strict: true,              // only accept objects and arrays (default)
  type: "application/json",  // which Content-Type to parse (default)
}));
```

<br><br>

### Return JSON Errors for Bad Bodies

```js
app.use((err, req, res, next) => {
  if (err.type === "entity.parse.failed") {
    return res.status(400).json({ error: "Invalid JSON" });
  }
  if (err.type === "entity.too.large") {
    return res.status(413).json({ error: "Body too large" });
  }
  next(err);
});
```

<br><br>

### Sibling Parsers

| Middleware             | Parses                              | Use for                                  |
| :--------------------- | :---------------------------------- | :--------------------------------------- |
| `express.json()`       | `application/json`                  | APIs                                     |
| `express.urlencoded()` | `application/x-www-form-urlencoded` | HTML form posts                          |
| `express.text()`       | `text/plain`                        | Plain text bodies                        |
| `express.raw()`        | Body as a `Buffer` (set `type`)     | Webhooks that verify signatures (Stripe) |
| `multer` (package)     | `multipart/form-data`               | File uploads                             |

<br><br>

### Key Points

- `express.json()` = parse JSON body into `req.body`. Built in since Express 4.16, no `body-parser` install needed.
- Only runs for matching `Content-Type`. Clients must send `application/json`.
- Default `limit` is **100kb**. Raise it deliberately, it protects against huge payloads.
- Parsed does not mean valid. **Validate** `req.body` (e.g. with Zod) before using it.
- In Express 5, `req.body` is `undefined` (not `{}`) when nothing was parsed.

<br><br>

## Other Ways to Ask This Question

- Why is `req.body` undefined in Express?
- What is the difference between `express.json()` and `body-parser`?
- What is the difference between `express.json()` and `express.urlencoded()`?
- How do you limit request body size in Express?
- What happens when a client sends invalid JSON to an Express API?
- Why do Stripe webhooks need `express.raw()` instead of `express.json()`?
