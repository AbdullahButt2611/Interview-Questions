# TTL Jitter

## Question

Why should TTLs have jitter?

## Answer

<mark>Keys cached at the same time with the same TTL also expire at the same time. That sends a burst of cache misses to the database (a cache avalanche). Adding a small random offset to each TTL spreads expiries out.</mark>

<br><br>

### The Problem

```ini
10:00:00  deploy warms the cache: 50,000 keys, all with EX 3600
11:00:00  all 50,000 keys expire in the same second
11:00:00  50,000 misses -> 50,000 Mongo queries -> DB spike
12:00:00  they were all re-cached together -> spike AGAIN
```

- Common triggers:
  - Cache warmup after a deploy or Redis restart.
  - A batch job caching many items in one loop.
  - Traffic peaks caching the same set of keys together.
- The spike **repeats every TTL**, because keys stay synchronized.

<br><br>

### The Fix

```js
// base TTL +/- 10%
const withJitter = (seconds, pct = 0.1) =>
  Math.round(seconds * (1 + (Math.random() * 2 - 1) * pct));

await redis.set(key, JSON.stringify(value), "EX", withJitter(3600));   // 3240s to 3960s
```

```ini
Without jitter:   all expire at 11:00:00
With +/-10%:      expiries spread over 10:54 to 11:06  -> smooth, small load
```

<br><br>

### Choosing the Amount

| Base TTL | Typical jitter | Expiry spread |
| :------- | :------------- | :------------ |
| 60 s     | +/- 10-20%     | ~12 to 24 s   |
| 1 hour   | +/- 10%        | ~12 minutes   |
| 1 day    | +/- 5-10%      | ~2 to 5 hours |

- Enough to spread load, small enough that data freshness barely changes.
- If data must **never** be older than X, use only **negative** jitter (`X * (0.9 to 1.0)`).

<br><br>

### Jitter vs Stampede Protection

- **Jitter** fixes **many different keys** expiring together (avalanche).
- It does **not** help **one hot key** with thousands of readers. That needs a lock or single-flight (see Cache Stampede).
- Use both.

<br><br>

### Key Points

- Same TTL + same write time = same expiry time = DB spike.
- Add **random jitter** (about 10%) to every TTL.
- The same idea applies to **retries** (backoff with jitter) and **cron jobs**, so clients do not all retry or run at once. ioredis 6's default reconnect strategy already adds jitter.

<br><br>

## Other Ways to Ask This Question

- What is a cache avalanche, and how do you prevent it?
- Why does the database spike at regular intervals after a deploy?
- How do you choose a TTL for cache keys?
- Why do retry strategies add random jitter?
- Stampede vs avalanche: what is the difference?
