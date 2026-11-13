# Redis Down Behavior

## Question

Redis is down. What does `/redis` do?

```js
const redis = new Redis(process.env.REDIS_URL || "redis://localhost:6379");

app.get("/redis", async (req, res) => {
  const reply = await redis.ping();
  res.json({ redis: reply });
});
```

## Answer

<mark>The request hangs. ioredis queues the PING and keeps reconnecting. Only after maxRetriesPerRequest (20) fails does the promise reject, and Express 5 then sends a generic 500.</mark>

<br><br>

### Step by Step

```ini
1. Request arrives, redis.ping() is called
2. Not connected -> PING goes into the offline queue (enableOfflineQueue: true)
3. ioredis retries the connection with backoff: 50ms, 100ms, 200ms ... up to 5s each
4. After 20 failed retries -> queued PING rejected with MaxRetriesPerRequestError
5. await throws -> Express 5 catches it -> default error handler -> 500
```

- With ioredis 6 defaults this wait is roughly **1 to 2 minutes**.
- The browser or a load balancer often **times out first**.
- If Redis comes back during the wait, the PING succeeds late and the user gets a slow `{"redis":"PONG"}`.

<br><br>

### What the Client Sees

```ini
HTTP 500 Internal Server Error    (HTML page, not JSON)
```

- The server logs show:

```ini
MaxRetriesPerRequestError: Reached the max retries per request limit (which is 20).
[ioredis] Unhandled error event: Error: connect ECONNREFUSED 127.0.0.1:6379
```

- The second line repeats on **every** reconnect attempt, because there is no `redis.on("error")` listener.

<br><br>

### Express 4 vs Express 5

| Version   | Rejected async handler                                         |
| :-------- | :------------------------------------------------------------- |
| Express 4 | Not caught. Unhandled rejection, request hangs or Node crashes |
| Express 5 | Caught and passed to the error handler, returns 500            |

<br><br>

### Problems

- **No timeout:** a health check that takes a minute is useless.
- **Wrong status:** 500 (server bug) instead of 503 (dependency unavailable).
- **Wrong format:** HTML error page from a JSON endpoint.
- **Log spam:** no `error` listener on the client.
- **Pile-up:** every request waits in the queue, holding sockets and memory.

<br><br>

### Fix: Fail Fast with a Clear Error

```js
const redis = new Redis(REDIS_URL, {
  maxRetriesPerRequest: 1,   // give up on a command quickly
  commandTimeout: 1000,      // reject any command after 1s
});

redis.on("error", (err) => console.error("Redis error:", err.message));

app.get("/redis", async (req, res) => {
  try {
    res.json({ redis: await redis.ping() });
  } catch (err) {
    res.status(503).json({ redis: "down", error: err.message });
  }
});
```

- Response now comes back in about **1 second** as a JSON **503**.
- For instant failure, also set `enableOfflineQueue: false` (commands fail at once while disconnected).

<br><br>

### Key Points

- ioredis's defaults favor **waiting and retrying**, not failing fast.
- Tune `maxRetriesPerRequest`, `commandTimeout` and `enableOfflineQueue` for request paths.
- Always add a client `error` listener and return **503** for a down dependency.
- The client keeps reconnecting in the background, so once Redis is back, requests work again with no restart.

<br><br>

## Other Ways to Ask This Question

- What happens to ioredis commands while Redis is disconnected?
- What is the ioredis offline queue, and when should you disable it?
- What does `maxRetriesPerRequest` control in ioredis?
- How do you add a timeout to Redis commands in Node.js?
- Should a health check return 500 or 503 when a dependency is down?
- What happens when an `async` Express handler throws, in Express 4 vs 5?
