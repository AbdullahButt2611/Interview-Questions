# Distributed Lock with Redis

## Question

How would you implement a distributed lock? What are Redlock's caveats?

## Answer

<mark>Acquire with SET key token NX PX ttl (only if free, auto-expires). Release with a Lua script that deletes the key only if it still holds your token. Redlock spreads this over several Redis nodes, but it relies on timing assumptions, so it is not safe when correctness truly matters.</mark>

<br><br>

### Single-Instance Lock

```js
const RELEASE = `
  if redis.call("GET", KEYS[1]) == ARGV[1] then
    return redis.call("DEL", KEYS[1])
  end
  return 0`;

const key = "lock:invoice:42";
const token = crypto.randomUUID();

const ok = await redis.set(key, token, "PX", 30000, "NX");   // acquire
if (!ok) return;                                              // someone else holds it

try {
  await generateInvoice(42);
} finally {
  await redis.eval(RELEASE, 1, key, token);                   // release only if still ours
}
```

<br><br>

### Why Each Part Matters

| Part             | Without it                                                          |
| :--------------- | :------------------------------------------------------------------ |
| `NX`             | Two clients overwrite each other, both "get" the lock               |
| `PX 30000` (TTL) | Holder crashes, lock is stuck **forever**                           |
| Random `token`   | Client A's lock expires, B takes it, A's `DEL` removes **B's** lock |
| Lua release      | `GET` then `DEL` separately can race, same problem as above         |

- Long jobs: **extend** the TTL while working (Lua: `PEXPIRE` only if the token matches).

<br><br>

### The Big Problem: The Lock Can Expire While You Work

```ini
t0   A acquires lock (TTL 30s)
t1   A pauses: GC pause, slow network, VM freeze (35s)
t31  lock expires, B acquires it
t35  A wakes up, still thinks it holds the lock  -> A and B both write
```

- **Fencing token** fix: every lock grant gets an increasing number (e.g. `INCR`). The storage **rejects** writes with an older number than it has already seen.
- A plain Redis lock does **not** give you fencing tokens.

<br><br>

### Redlock (Multi-Node)

- Solves: a single master crashing **before** the lock replicates to its replica (async replication), so a new master has no lock.

```ini
1. Use N = 5 independent Redis masters (no replication between them)
2. Try SET NX PX on all 5 with the same token, short timeouts
3. Lock acquired if a majority (3+) succeeded
   AND time taken < TTL
4. Valid time = TTL - time taken - clock drift
5. Release on all 5 nodes
```

<br><br>

### Redlock's Caveats

- **Timing assumptions:** it assumes bounded network delay, bounded process pauses and roughly correct clocks. Real systems break all three.
- **Process pauses:** a GC pause past the TTL still gives **two holders**, exactly like the single-node case.
- **Clock jumps:** if a node's clock jumps forward (NTP fix), its key expires early, and a majority can form for a second client.
- **Node restarts:** a node that restarts without persisting the key (no `fsync always`) "forgets" the lock. Needs a delayed restart.
- **No fencing tokens**, so it cannot protect the resource itself.
- These points come from Martin Kleppmann's critique (2016). antirez (Redis author) replied, and the debate is a common interview topic.

<br><br>

### Which Lock to Use

| Goal                                                       | Use                                                                              |
| :--------------------------------------------------------- | :------------------------------------------------------------------------------- |
| **Efficiency**: avoid duplicate work (cron, cache rebuild) | Single Redis lock (`SET NX PX`), rare double run is OK                           |
| **Correctness**: two holders would corrupt data            | ZooKeeper / etcd + **fencing tokens**, or DB transactions and unique constraints |

<br><br>

### Key Points

- Acquire: `SET key token NX PX ttl`. Release: **Lua compare-and-delete**.
- TTL prevents deadlocks, but a paused client can outlive its lock.
- Redlock adds fault tolerance, not **correctness**. It still depends on timing.
- For correctness, use **fencing tokens** with a consensus system, or let the database enforce it.

<br><br>

## Other Ways to Ask This Question

- How do you make sure only one server runs a cron job at a time?
- Why must a Redis lock have a random value and a TTL?
- Why do you release a Redis lock with a Lua script?
- What is a fencing token?
- What is Redlock, and why did Martin Kleppmann criticize it?
- Redis lock vs ZooKeeper/etcd lock: when would you use each?
