# Cache Stampede (Thundering Herd)

## Question

What is a cache stampede (thundering herd)? How do you prevent it?

## Answer

<mark>A hot key expires, and hundreds of requests miss the cache at the same moment. They all hit the database to rebuild the same value, overloading it. Prevent it by letting only one request rebuild (lock or single-flight), refreshing early, or serving stale data while refreshing.</mark>

<br><br>

### What Happens

```ini
t0   "product:42" expires              (read 1,000 times per second)
t0   1,000 requests miss the cache
t0   1,000 identical queries hit Mongo  -> CPU spikes, queries slow down
t1   slow queries -> timeouts -> retries -> even more load
t2   DB falls over, the whole app is down
```

- Same effect when the cache is **empty**: after a deploy, a Redis restart, or `FLUSHALL`.
- Related: **cache avalanche**, when many keys expire at once because they share the same TTL.

<br><br>

### Prevention Techniques

| Technique                   | Idea                                              | Scope            |
| :-------------------------- | :------------------------------------------------ | :--------------- |
| Single-flight (coalescing)  | Concurrent misses share one in-flight promise     | One app instance |
| Distributed lock (`SET NX`) | Only the lock holder rebuilds, others wait        | All instances    |
| Serve stale, refresh behind | Return old value while one request refreshes      | All instances    |
| Early / background refresh  | Rebuild **before** the key expires                | Hot keys         |
| TTL jitter                  | Random TTL spread, so keys do not expire together | Avalanche        |

<br><br>

### 1. Single-Flight (Per Instance)

```js
const inflight = new Map();

async function getCached(key, ttl, load) {
  const hit = await redis.get(key);
  if (hit) return JSON.parse(hit);

  if (!inflight.has(key)) {
    inflight.set(key, (async () => {
      try {
        const value = await load();
        await redis.set(key, JSON.stringify(value), "EX", ttl);
        return value;
      } finally {
        inflight.delete(key);
      }
    })());
  }
  return inflight.get(key);   // everyone awaits the same promise
}
```

- 1,000 misses on one instance = **1** DB query.
- With 10 instances, still up to 10 queries. Combine with a lock for full protection.

<br><br>

### 2. Distributed Lock (All Instances)

```js
const token = crypto.randomUUID();
const locked = await redis.set(`lock:${key}`, token, "PX", 5000, "NX");

if (locked) {
  // rebuild, cache it, then release only if we still own the lock
} else {
  // wait ~50ms and read the cache again, or serve a stale copy
}
```

- `NX` = set only if not exists. `PX 5000` = auto-expire, so a crashed holder cannot block forever.
- Release with a check-and-delete **Lua script**, so you never delete someone else's lock.

<br><br>

### 3. Serve Stale While Refreshing

- Store the value with a **logical expiry** inside it, and a longer real TTL in Redis.
- After the logical expiry, return the old value **and** let one request refresh it in the background.
- Users never wait on the database for hot keys.

<br><br>

### Key Points

- Stampede = **many misses for the same key at once**, all rebuilding it.
- Core fix: **only one rebuild**. Single-flight per instance, a lock across instances.
- For very hot keys, refresh early or serve stale, so they never truly expire.
- Add **TTL jitter** so many keys do not expire in the same second.

<br><br>

## Other Ways to Ask This Question

- What happens when a popular cache key expires under heavy traffic?
- What is the dogpile effect?
- How do you stop 1,000 requests from rebuilding the same cache entry?
- What is request coalescing / single-flight?
- How do you use `SET NX PX` as a lock in Redis?
- What is the difference between a cache stampede and a cache avalanche?
