# Missing Redis Error Listener

## Question

There's no `redis.on('error')` listener. Why does that matter?

```js
const redis = new Redis(process.env.REDIS_URL || "redis://localhost:6379");
// no redis.on("error", ...)
```

## Answer

<mark>In Node, an EventEmitter that emits 'error' with no listener throws and can crash the process. ioredis avoids the crash, but spams the console and gives your app no way to react.</mark>

<br><br>

### The Node.js Rule

```ini
emitter.emit("error", err)
  listener exists -> listener runs
  no listener     -> err is thrown -> uncaught exception -> process exits
```

- `"error"` is the **only** event Node treats this way.
- Applies to sockets, streams, servers and most DB clients.

<br><br>

### What Each Redis Client Does

| Client                 | No `error` listener and Redis goes down                 |
| :--------------------- | :------------------------------------------------------ |
| node-redis (`redis`)   | Error is thrown, **process crashes**                    |
| ioredis (this project) | Prints `[ioredis] Unhandled error event`, keeps running |

- ioredis checks for listeners first. If none, it calls `console.error` instead of `emit`.
- Other clients (and future code) may not be that forgiving.

<br><br>

### Why It Still Matters with ioredis

- **Log spam:** a full stack trace on **every** reconnect attempt, every few seconds, for as long as Redis is down.

```ini
[ioredis] Unhandled error event: Error: connect ECONNREFUSED 127.0.0.1:6379
[ioredis] Unhandled error event: Error: connect ECONNREFUSED 127.0.0.1:6379
...
```

- **No control:** cannot send it to your logger, metrics or alerting.
- **No reaction:** app cannot mark itself degraded, flip a health flag, or skip the cache.
- **Hidden misconfig:** wrong password (`WRONGPASS`) looks the same as a network blip in raw console output.

<br><br>

### Fix

```js
const redis = new Redis(REDIS_URL);

redis.on("error", (err) => console.error("Redis error:", err.message));
redis.on("reconnecting", (ms) => console.warn(`Redis reconnecting in ${ms}ms`));
redis.on("ready", () => console.log("Redis ready"));
```

- Attach it **right after** creating the client, before any connect attempt fires.
- Keep the handler cheap. Do **not** throw inside it.
- Do **not** `process.exit()` on transient errors. The client reconnects by itself.

<br><br>

### Key Points

- Unhandled `"error"` event = crash in plain Node. Always add a listener.
- ioredis is lenient, but the listener is still how you **log, alert and degrade gracefully**.
- Same rule applies to every long-lived connection: Mongo, sockets, streams, HTTP servers.

<br><br>

## Other Ways to Ask This Question

- What happens when an EventEmitter emits `error` with no listener?
- Why does my app print `[ioredis] Unhandled error event`?
- Why did my Node app crash when Redis restarted?
- Which ioredis events would you listen to in production?
- Should you exit the process when the Redis connection fails?
