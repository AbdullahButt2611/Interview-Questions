# Async Error Handling: Express 4 vs 5

## Question

In Express 5, what happens when an `async` handler throws? How did Express 4 differ?

```js
app.get("/redis", async (req, res) => {
  const reply = await redis.ping();   // what if this throws?
  res.json({ redis: reply });
});
```

## Answer

<mark>Express 5 catches the rejected promise and calls next(err) for you, so the error handler sends a response. Express 4 ignored the promise: the request hung and the rejection went unhandled (crashing Node 15+).</mark>

<br><br>

### Express 5

```ini
async handler throws
  -> returns a rejected promise
  -> Express sees it, calls next(err)
  -> error-handling middleware (or default handler) responds
```

- Default handler sends **500** (or `err.status` / `err.statusCode` if set).
- In development it shows the stack trace. With `NODE_ENV=production` it hides it.
- Rejected with no value? Express passes a default `Error` instead.

<br><br>

### Express 4

```ini
async handler throws
  -> returns a rejected promise
  -> Express ignores the return value
  -> no response is ever sent, request hangs
  -> "unhandledRejection" -> Node 15+ crashes the whole process
```

- **Sync** throws were always caught in Express 4. Only **async** errors were lost.

<br><br>

### Comparison

| Situation                            | Express 4                     | Express 5                     |
| :----------------------------------- | :---------------------------- | :---------------------------- |
| Sync `throw` in handler              | Caught, goes to error handler | Caught, goes to error handler |
| `async` handler throws / rejects     | **Not caught**, request hangs | Caught, `next(err)` called    |
| Error inside `setTimeout` / callback | Not caught                    | Not caught                    |
| Need try/catch or wrapper            | Yes                           | No                            |

<br><br>

### Express 4 Workarounds

```js
// 1. try/catch in every handler
app.get("/redis", async (req, res, next) => {
  try {
    res.json({ redis: await redis.ping() });
  } catch (err) {
    next(err);
  }
});

// 2. Wrapper
const asyncHandler = (fn) => (req, res, next) =>
  Promise.resolve(fn(req, res, next)).catch(next);

app.get("/redis", asyncHandler(async (req, res) => { /* ... */ }));

// 3. Patch package
import "express-async-errors";
```

<br><br>

### Custom Error Handler (Both Versions)

```js
app.use((err, req, res, next) => {          // 4 arguments = error handler
  console.error(err);
  res.status(err.status ?? 500).json({ error: err.message });
});
```

- Register it **after** all routes.
- Returns JSON instead of the default HTML error page.

<br><br>

### Key Points

- Express 5 only catches the promise the handler **returns**. A promise you start but do not `await` can still reject unhandled.
- Errors in plain callbacks (`setTimeout`, old-style `fs` callbacks) still need `next(err)` manually.
- Upgrading to Express 5 lets you **delete** `asyncHandler` wrappers and `express-async-errors`.

<br><br>

## Other Ways to Ask This Question

- How do you handle errors in async Express routes?
- Why does my Express 4 request hang when an `await` fails?
- What does `express-async-errors` do?
- How do you write an error-handling middleware in Express?
- What changed in error handling from Express 4 to Express 5?
- What happens to an unhandled promise rejection in Node.js 15+?
