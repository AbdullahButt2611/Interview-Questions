# res.json() vs res.send()

## Question

What does `res.json()` do that `res.send()` doesn't?

## Answer

<mark>res.json() always sends valid JSON: it serializes any value and sets Content-Type: application/json. res.send() picks the type based on the value.</mark>

- For **objects and arrays**, both behave the same. `res.send(obj)` calls `res.json(obj)` internally.
- The difference shows with **strings, null and numbers**.

<br><br>

### How Each One Decides

```ini
res.json(value)
  1. JSON.stringify(value)  (uses app "json spaces", "json replacer", "json escape")
  2. Content-Type: application/json
  3. res.send(jsonString)

res.send(value)
  string          -> sent as-is,   Content-Type: text/html
  Buffer          -> sent as-is,   Content-Type: application/octet-stream
  object / array  -> calls res.json()
```

<br><br>

### Where They Differ

| Call                     | Body sent     | Content-Type               |
| :----------------------- | :------------ | :------------------------- |
| `res.send({ ok: true })` | `{"ok":true}` | `application/json`         |
| `res.json({ ok: true })` | `{"ok":true}` | `application/json`         |
| `res.send("PONG")`       | `PONG`        | `text/html`                |
| `res.json("PONG")`       | `"PONG"`      | `application/json`         |
| `res.send(null)`         | empty         | none                       |
| `res.json(null)`         | `null`        | `application/json`         |

- A client calling `await response.json()` on `res.send("PONG")` will **fail to parse** it.

<br><br>

### Formatting Through App Settings

```js
app.set("json spaces", 2);                  // pretty-print
app.set("json replacer", (k, v) => (k === "password" ? undefined : v));
```

- Only `res.json()` (and `res.send` with objects, since it calls `res.json`) uses these.

<br><br>

### Example

```js
app.get("/redis", async (req, res) => {
  const pong = await redis.ping();   // "PONG"
  res.json({ redis: pong });         // {"redis":"PONG"}, application/json
});
```

<br><br>

### Key Points

- Building a JSON API: use **`res.json()`** every time. Clear intent, consistent output.
- Sending HTML, plain text or a file buffer: use **`res.send()`**.
- Both end the response. Do not call a second `res.send` / `res.json` after it (`ERR_HTTP_HEADERS_SENT`).
- Express 5 removed `res.send(statusCode)`. Use `res.sendStatus(200)` or `res.status(200).json(...)`.

<br><br>

## Other Ways to Ask This Question

- What is the difference between `res.send()`, `res.json()` and `res.end()` in Express?
- Why is my Express response coming back as `text/html` instead of JSON?
- What Content-Type does `res.send()` set for a string?
- How do you pretty-print JSON responses in Express?
- What causes "Cannot set headers after they are sent to the client"?
