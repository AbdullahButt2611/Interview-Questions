# ioredis Offline Queue

## Question

What is ioredis's offline queue? When should you disable it?

## Answer

<mark>The offline queue buffers commands while the client is not connected (or not ready yet), then sends them once the connection is up. Disable it when you would rather fail immediately than wait, like on HTTP request paths and health checks.</mark>

- Option: `enableOfflineQueue` (default `true`).

<br><br>

### How It Works

```ini
redis.get("x") called
  connection ready?  Yes -> sent now
                     No  -> pushed into the offline queue
                            ... reconnect succeeds -> queue flushed, command sent
                            ... retries run out    -> command rejected (MaxRetriesPerRequestError)
```

- Covers **startup** too: commands called right after `new Redis()`, before the connection is ready, wait in the queue.
- That is why `/redis` in this project can run before Redis is connected and still work.

<br><br>

### With It Disabled

```js
const redis = new Redis(REDIS_URL, { enableOfflineQueue: false });

await redis.get("x");
// while disconnected -> rejects immediately:
// Error: Stream isn't writeable and enableOfflineQueue options is false
```

<br><br>

### Enabled vs Disabled

| Aspect              | Enabled (default)                     | Disabled                              |
| :------------------ | :------------------------------------ | :------------------------------------ |
| Redis briefly down  | Commands wait, then succeed           | Commands fail instantly               |
| Redis down for long | Requests hang until retries run out   | Fast error, app can fall back         |
| Startup             | Can send commands before `ready`      | Must wait for the `ready` event first |
| Memory              | Queue grows while down (all callers)  | Nothing queued                        |
| Best for            | Workers, background jobs, short blips | HTTP requests, caches, health checks  |

<br><br>

### When to Disable

- **HTTP request paths:** a user should get a fast fallback or a 503, not a 60-second hang.
- **Cache lookups:** on failure, skip the cache and read from the database.
- **Health checks:** must report "down" right away.
- **High traffic:** thousands of queued commands during an outage use memory and then hit Redis all at once on reconnect.

<br><br>

### When to Keep It

- **Background workers** (e.g. BullMQ `Worker`): waiting through a short blip is better than failing jobs. BullMQ itself recommends the opposite for `Queue` producers called from HTTP handlers.
- **Startup code** that sends commands before the connection is ready.
- **Writes that must not be dropped** and can tolerate delay.

<br><br>

### Disabling Safely

```js
const redis = new Redis(REDIS_URL, { enableOfflineQueue: false });

await new Promise((resolve, reject) => {
  redis.once("ready", resolve);
  redis.once("error", reject);
});   // wait at boot, so early commands do not fail

app.listen(3000);
```

<br><br>

### Key Points

- Offline queue = **wait for the connection** instead of failing.
- Good for resilience, bad for latency. Requests can **hang** while Redis is down.
- Disable it for request paths. Then wait for `ready` at startup.
- Related knobs: `maxRetriesPerRequest` (how long queued commands wait) and `commandTimeout` (per-command limit).

<br><br>

## Other Ways to Ask This Question

- What happens to ioredis commands while Redis is disconnected?
- What does "Stream isn't writeable and enableOfflineQueue options is false" mean?
- How do you make ioredis fail fast instead of waiting?
- Why do my requests hang when Redis is down?
- Should a cache client queue commands during an outage?
