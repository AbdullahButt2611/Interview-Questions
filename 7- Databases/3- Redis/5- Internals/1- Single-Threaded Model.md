# Single-Threaded Model

## Question

Redis is single-threaded. Why is that fast, and what breaks it?

## Answer

<mark>One thread runs every command, one at a time, against data in RAM, using an event loop for I/O. No locks and no context switches make each command very fast. Anything slow (a big O(N) command, a long Lua script, deleting a huge key) blocks every other client.</mark>

<br><br>

### Why One Thread Is Fast

- **In-memory data:** no disk reads, so most commands finish in **microseconds**.
- **No locks:** no thread waits for another, no lock contention.
- **No context switches:** the CPU stays on one hot loop with warm caches.
- **Atomic for free:** every command runs alone, so no race conditions inside a command.
- **Event loop (`epoll`):** one thread watches thousands of sockets and only handles the ready ones.
- Usually limited by **network and memory**, not CPU.

<br><br>

### Not Everything Is Single-Threaded

| Work                                  | Thread                 |
| :------------------------------------ | :--------------------- |
| Running commands                      | **Main thread** (one)  |
| Network reads/writes (Redis 6+)       | I/O threads (optional) |
| `UNLINK`, `FLUSHALL ASYNC`, lazy free | Background threads     |
| AOF fsync, closing files              | Background threads     |
| RDB snapshot, AOF rewrite             | Forked child process   |

<br><br>

### What Breaks It

```ini
Client A:  KEYS *            (10 million keys, 2 seconds)
Client B:  GET user:1        waits 2 seconds
Client C:  SET x 1           waits 2 seconds
... every client is frozen until A finishes
```

| Cause                                             | Fix                                       |
| :------------------------------------------------ | :---------------------------------------- |
| `KEYS *` on a large database                      | `SCAN` with a cursor                      |
| `HGETALL`, `SMEMBERS`, `LRANGE 0 -1` on huge keys | `HSCAN`, `SSCAN`, ranged reads            |
| `DEL` on a key with millions of items             | `UNLINK` (frees memory in the background) |
| `FLUSHALL` / `FLUSHDB`                            | `FLUSHALL ASYNC`                          |
| Long Lua scripts or big `MULTI` blocks            | Keep scripts short, split the work        |
| Huge values (MB-sized strings)                    | Split into smaller keys, compress         |
| `fork()` for RDB/AOF on a large dataset           | Leave memory headroom, schedule snapshots |
| Swapping to disk                                  | Set `maxmemory`, disable swap             |
| One CPU core maxed out                            | Shard (Redis Cluster), read replicas      |

<br><br>

### How to Find the Culprit

```bash
redis-cli SLOWLOG GET 10        # slowest recent commands
redis-cli --bigkeys             # largest keys per type
redis-cli --latency             # live latency from your machine
redis-cli LATENCY DOCTOR        # Redis's own latency report
redis-cli INFO commandstats     # time spent per command type
```

<br><br>

### Key Points

- Single-threaded **execution** = fast, simple, atomic. Not "single-threaded everything".
- The rule: **no slow commands**. One slow command is slow for everyone.
- Prefer `SCAN` over `KEYS`, `UNLINK` over `DEL` on big keys, `ASYNC` flushes.
- Scale beyond one core with **sharding**, not more threads.

<br><br>

## Other Ways to Ask This Question

- How can a single-threaded database handle 100,000+ operations per second?
- Why should you never run `KEYS *` in production?
- What is the difference between `DEL` and `UNLINK`?
- What did Redis 6 I/O threads change?
- How do you find slow commands in Redis?
- How do you scale Redis when one CPU core is not enough?
