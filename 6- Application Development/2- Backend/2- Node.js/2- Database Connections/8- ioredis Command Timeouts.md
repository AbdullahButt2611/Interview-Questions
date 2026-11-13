# ioredis Command Timeouts

## Question

How do you set per-command timeouts in ioredis?

## Answer

<mark>Use the commandTimeout option. It applies to every command on that client: if no reply arrives within N ms, the promise rejects with "Command timed out". For a different timeout per command, use a second client or wrap the call.</mark>

```js
const redis = new Redis(REDIS_URL, { commandTimeout: 1000 });

await redis.get("user:1");   // rejects after 1s: Error: Command timed out
```

- Default: **no** command timeout. A command can wait as long as retries allow.

<br><br>

### All Timeout-Related Options

| Option                 | Default  | What it limits                                         |
| :--------------------- | :------- | :----------------------------------------------------- |
| `commandTimeout`       | none     | Time to wait for **each command's** reply              |
| `connectTimeout`       | 10000 ms | Time to establish the TCP connection                   |
| `socketTimeout`        | none     | Silence on a socket before it is treated as dead       |
| `maxRetriesPerRequest` | 20       | Reconnect attempts before queued commands are rejected |
| `enableOfflineQueue`   | true     | Queue commands while disconnected (false = fail now)   |
| `blockingTimeout`      | none     | Client-side safety net for `BLPOP`, `XREAD BLOCK`      |

- A production-friendly combination for request paths:

```js
const redis = new Redis(REDIS_URL, {
  commandTimeout: 1000,
  maxRetriesPerRequest: 1,
  connectTimeout: 5000,
});
```

<br><br>

### Different Timeouts for Different Commands

ioredis has **no per-call timeout argument**. Options:

**1. A second client with its own settings**

```js
const fast = new Redis(REDIS_URL, { commandTimeout: 200 });   // cache reads
const slow = fast.duplicate({ commandTimeout: 5000 });        // batch jobs, big scans
```

**2. Wrap a single call**

```js
const withTimeout = (p, ms) =>
  Promise.race([p, new Promise((_, rej) => setTimeout(() => rej(new Error("timeout")), ms))]);

const value = await withTimeout(redis.get("report:2026"), 3000);
```

**3. Blocking commands: pass the timeout to Redis**

```js
await redis.blpop("jobs", 5);   // server waits at most 5 seconds
```

<br><br>

### Important Catch

- A timeout only stops **the client waiting**. It does **not** cancel the command on the server.
- A timed-out `SET` or `INCR` may **still have been applied**. Retrying it blindly can double-count.
- Keep timeouts on writes generous, and make retried writes **idempotent**.

<br><br>

### Key Points

- `commandTimeout` = per-command limit, set once per **client**.
- Pair it with low `maxRetriesPerRequest` so requests fail fast when Redis is down.
- Need different limits? Use `duplicate()` with new options, or wrap the promise.
- Timeouts protect the **app**, not the data. The server may finish the command anyway.

<br><br>

## Other Ways to Ask This Question

- How do you stop a Redis call from hanging forever in Node.js?
- What is the difference between `connectTimeout` and `commandTimeout` in ioredis?
- What does "Command timed out" mean in ioredis?
- If a Redis write times out, did it happen or not?
- How do you use different timeout settings for different Redis workloads?
