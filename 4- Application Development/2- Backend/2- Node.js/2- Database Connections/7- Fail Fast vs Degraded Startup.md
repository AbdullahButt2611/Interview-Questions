# Fail Fast vs Degraded Startup

## Question

Should the app crash on startup if Redis is unreachable, or start degraded?

## Answer

<mark>It depends on Redis's role. If Redis is only a cache, start degraded and fall back to the database. If Redis holds required data (sessions, queues, locks), fail fast and exit.</mark>

- The real question is: **can the app still do its job correctly without Redis?**

<br><br>

### Decide by Role

| Redis is used for       | Without Redis                              | Startup choice     |
| :---------------------- | :----------------------------------------- | :----------------- |
| Cache in front of Mongo | Slower, but correct                        | **Start degraded** |
| Sessions / login tokens | Every user is logged out                   | **Fail fast**      |
| Job queue (BullMQ)      | Jobs lost or never processed               | **Fail fast**      |
| Distributed locks       | Duplicate work, data races                 | **Fail fast**      |
| Rate limiting           | Fail open (no limit) or closed (block all) | Business decision  |

<br><br>

### Fail Fast

```js
try {
  await redis.ping();
} catch (err) {
  console.error("Redis required but unreachable:", err.message);
  process.exit(1);   // Docker / Kubernetes restarts the app with backoff
}
```

**Pros**

- Misconfiguration is caught **at deploy**, not by users.
- No half-working app serving wrong results.

**Cons**

- A Redis outage takes the **whole app** down.
- Needs a short retry window at boot, or startup ordering issues cause crash loops.

<br><br>

### Start Degraded

```js
try {
  await redis.ping();
} catch {
  console.warn("Redis unavailable, starting without cache");   // log and keep going
}
```

```js
async function cached(key, ttl, load) {
  if (redis.status === "ready") {
    const hit = await redis.get(key).catch(() => null);
    if (hit) return JSON.parse(hit);
  }
  const value = await load();                                   // read from Mongo
  redis.set(key, JSON.stringify(value), "EX", ttl).catch(() => {});
  return value;
}
```

**Pros**

- App stays **available**, only slower.
- ioredis keeps reconnecting, so the cache comes back on its own.

**Cons**

- All load now hits Mongo, which can **overload** it (cascading failure).
- Degraded state can go unnoticed without alerts.

<br><br>

### Make It Visible Either Way

- Log a clear warning and **alert** when running degraded.
- Report it in the health check (`"redis": "down"`, overall `"degraded"`).
- Use fail-fast client options (`commandTimeout`, low `maxRetriesPerRequest`) so cache misses do not hang.

<br><br>

### Key Points

- **Optional dependency** (cache) = degrade gracefully. **Required dependency** = fail fast.
- A good default: retry briefly at boot (e.g. 30 seconds), then decide based on the role.
- Make it configurable (`REDIS_REQUIRED=true`) if the role differs per environment.
- Degraded mode must protect the database, or one outage turns into two.

<br><br>

## Other Ways to Ask This Question

- What is graceful degradation?
- What does "fail fast" mean, and when is it the right choice?
- What happens to your app if the cache goes down?
- Should a rate limiter fail open or fail closed?
- How do you stop a cache outage from taking down the database?
- Hard dependency vs soft dependency: how do you treat each?
