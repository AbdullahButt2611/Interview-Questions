# What is Redis and Why is it Fast

## Question

What is Redis? Why is it fast?

## Answer

<mark>Redis is an in-memory key-value data store. It is fast because data lives in RAM and commands run on a single-threaded event loop with no disk reads on the hot path.</mark>

<br><br>

### What is Redis

- **RE**mote **DI**ctionary **S**erver.
- Stores data as **key-value pairs** in **RAM**.
- Values are rich data structures, not just strings: String, List, Hash, Set, Sorted Set, Stream, and more.
- Can **persist** to disk (RDB snapshots, AOF log) so data survives restarts.

<br><br>

### Use Cases

| Use case            | Why Redis fits                                          | Redis feature                    |
| :------------------ | :------------------------------------------------------ | :------------------------------- |
| Caching             | Query results, page fragments, API responses from RAM   | String + TTL                     |
| Session management  | Fast read/write on every request, auto-expire on logout | Hash or String + TTL             |
| Real-time analytics | Very high write rate for counters and events            | `INCR`, HyperLogLog, Streams     |
| Leaderboards        | Always-sorted scores, top-N in one call                 | Sorted Set (`ZADD`, `ZREVRANGE`) |
| Counting            | Atomic increments, no race conditions                   | `INCR`, `HINCRBY`                |
| Rate limiting       | Shared counter across all app instances                 | `INCR` + `EXPIRE`, Sorted Set    |
| Message queuing     | Lightweight broker between services                     | Pub/Sub, Lists, **Streams**      |

- **Pub/Sub** is fire-and-forget: offline subscribers miss messages. For reliable queues use **Streams** (see Pub/Sub vs Streams vs Lists).
- **Analytics:** one instance handles **100,000+ ops/sec**. Millions per second needs pipelining or a cluster.
- Not a fit: data larger than RAM, complex queries and joins, or data that must never lose a write.

<br><br>

### Why is it Fast

**1. In-memory storage**

- Reads and writes hit RAM, not disk.

```ini
RAM access   ~ 100 nanoseconds
SSD access   ~ 100 microseconds   (about 1000x slower)
```

**2. Single-threaded command execution**

- One thread runs all commands, one at a time.
- **No locks**, no context switches, no race conditions between commands.
- Every command is **atomic** for free.

**3. I/O multiplexing (event loop)**

- Uses `epoll` (Linux) / `kqueue` (macOS) to watch thousands of connections at once.
- The thread never sits waiting on one slow client. It only handles sockets that are ready.

**4. Efficient data structures**

- Purpose-built internals: dynamic strings (SDS), hash tables, skip lists, compact encodings (listpack, intset) for small collections.
- Most commands are **O(1)** or **O(log n)**.

**5. Simple protocol**

- RESP (Redis Serialization Protocol) is plain text and cheap to parse.
- Supports **pipelining**: send many commands in one round trip.

**6. Persistence off the hot path**

- RDB snapshots and AOF rewrites run in a **forked child process**.
- AOF fsync defaults to once per second (`everysec`), not on every write.

<br><br>

### Single-Threaded: The Catch

- One slow command blocks **every** client.
- Avoid on large data: `KEYS *`, huge `SMEMBERS` / `HGETALL`, `FLUSHALL` (sync).
- Use `SCAN`, `SSCAN`, `HSCAN` instead to iterate in small batches.
- Redis 6+ added **I/O threads** for network reads and writes, but commands still run on one thread.

<br><br>

### Key Points

- Bottleneck in Redis is usually **network and memory**, not CPU.
- Data size is limited by **RAM**, so it is costlier per GB than a disk database.
- Speed comes from design: RAM + single thread + event loop + smart data structures.

<br><br>

## Other Ways to Ask This Question

- Redis is single-threaded. How can it be so fast?
- What makes Redis faster than a traditional database like MySQL or MongoDB?
- What is Redis and where would you use it?
- What are the common use cases of Redis?
- Why is Redis a good fit for sessions and leaderboards?
- How does Redis handle thousands of clients with one thread?
- Why should you avoid the `KEYS` command in production?
- What are the limitations of an in-memory database?
