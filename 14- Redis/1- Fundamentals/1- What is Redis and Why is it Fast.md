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
- Common uses:
  - Caching
  - Sessions
  - Rate limiting
  - Queues and Pub/Sub
  - Leaderboards (Sorted Sets)

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
- How does Redis handle thousands of clients with one thread?
- Why should you avoid the `KEYS` command in production?
- What are the limitations of an in-memory database?
