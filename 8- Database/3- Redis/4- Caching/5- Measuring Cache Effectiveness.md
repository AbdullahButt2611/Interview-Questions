# Measuring Cache Effectiveness

## Question

How do you measure whether the cache helps?

## Answer

<mark>Measure three things before and after adding the cache: hit ratio, request latency (p95/p99), and database load. A cache helps only if latency or DB load drops meaningfully, not just because the hit ratio looks high.</mark>

<br><br>

### The Core Metrics

| Metric              | Where to get it                     | Good sign                       |
| :------------------ | :---------------------------------- | :------------------------------ |
| Hit ratio           | App counters, or Redis `INFO stats` | High and stable (often 80%+)    |
| Latency p50/p95/p99 | APM, request logs, load tests       | Drops vs no cache               |
| DB load             | Mongo QPS, CPU, slow query log      | Drops vs no cache               |
| Evictions           | `INFO stats`: `evicted_keys`        | Near zero                       |
| Memory              | `INFO memory`: `used_memory_human`  | Below `maxmemory` with headroom |
| Staleness bugs      | Support tickets, bug reports        | None                            |

<br><br>

### Hit Ratio

```bash
redis-cli INFO stats | grep keyspace
# keyspace_hits:950000
# keyspace_misses:50000      -> 950000 / 1000000 = 95% hit ratio
```

- Redis numbers are **server-wide**: every key, every app. Fine for a quick look.
- For real answers, count hits and misses **in the app, per key type**:

```js
const hit = await redis.get(key);
metrics.increment(hit ? "cache.hit" : "cache.miss", { type: "product" });
```

<br><br>

### Latency: Do the Math

```ini
Without cache:  every request = 50 ms (Mongo)

With cache, 90% hit ratio:
  hit  = 1 ms
  miss = 1 ms (cache check) + 50 ms (Mongo) = 51 ms
  average = 0.9 x 1 + 0.1 x 51 = 6 ms     -> about 8x faster
```

- Look at **p95/p99**, not only the average. Misses live in the tail.
- A cache with a **low** hit ratio makes misses **slower** (extra round trip) and adds complexity.

<br><br>

### Prove It With a Comparison

- **Before/after:** record latency and DB load for a week, enable the cache, compare.
- **Feature flag:** bypass the cache for 5% of traffic and compare the two groups.
- **Load test:** same traffic with and without the cache.

<br><br>

### Warning Signs

| Symptom                         | Likely cause                                        |
| :------------------------------ | :-------------------------------------------------- |
| Low hit ratio                   | TTL too short, keys too unique, data rarely re-read |
| Rising `evicted_keys`           | `maxmemory` too small for the working set           |
| High hit ratio, no latency gain | The cached query was already cheap                  |
| DB spikes at regular intervals  | Keys expiring together, add TTL jitter              |
| Users see old data              | Missing invalidation, TTL too long                  |

<br><br>

### Key Points

- Track **hit ratio, p95/p99 latency, DB load**, before and after.
- Measure hit ratio **per key type in the app**. Redis's number mixes everything.
- A high hit ratio means nothing if the cached work was cheap.
- If the cache does not cut latency or DB load, remove it: it is extra complexity.

<br><br>

## Other Ways to Ask This Question

- What is a cache hit ratio, and what is a good one?
- How do you find the cache hit rate in Redis?
- Can a cache make an application slower?
- Why look at p99 latency instead of the average?
- Which Redis metrics would you put on a dashboard?
