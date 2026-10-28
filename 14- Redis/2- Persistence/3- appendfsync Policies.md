# appendfsync Policies

## Question

What are `appendfsync always / everysec / no`? Which is the default?

## Answer

<mark>They control how often Redis forces the AOF from memory onto the physical disk (fsync). Default is everysec: about 1 second of risk, with near full speed.</mark>

<br><br>

### write() vs fsync()

```ini
Redis appends to AOF  -> write()  -> data sits in the OS page cache (RAM)
                      -> fsync()  -> OS forces it onto the actual disk
```

- After `write()`, data survives a **Redis crash** (the OS still has it).
- Only after `fsync()` does it survive a **power cut or OS crash**.
- `appendfsync` decides **when** `fsync()` happens.

<br><br>

### The Three Options

| Policy               | When fsync runs                    | Max loss on power cut | Speed   |
| :------------------- | :--------------------------------- | :-------------------- | :------ |
| `always`             | After every write, before replying | ~0 (one batch)        | Slowest |
| `everysec` (default) | Once per second, background thread | ~1 second (up to 2)   | Fast    |
| `no`                 | Whenever the OS decides            | ~30 seconds on Linux  | Fastest |

<br><br>

### `always`

- Every write batch is fsynced **before** the client gets `OK`.
- Strongest durability, but each write waits for the disk. On slow disks, throughput drops sharply.
- Redis groups commands from one event loop cycle into **one fsync** (group commit) to soften the cost.

<br><br>

### `everysec` (default)

- A **background thread** runs fsync once per second. The main thread does not wait.
- If the disk is so slow that an fsync takes over 2 seconds, Redis **delays writes** and logs:

```ini
Asynchronous AOF fsync is taking too long (disk is busy?)
```

- Worst case loss is about **2 seconds**, usually 1.

<br><br>

### `no`

- Redis only calls `write()`. The OS flushes when it wants (Linux: around every 30 seconds).
- Fastest, but the weakest guarantee. Rarely worth it over `everysec`.

<br><br>

### How to Set It

```bash
redis-server --appendonly yes --appendfsync everysec   # CLI / Docker command
CONFIG SET appendfsync always                          # at runtime
CONFIG GET appendfsync                                 # check current value
```

<br><br>

### Key Points

- Default: **`everysec`**. The best balance for almost every workload.
- `always` only when every acknowledged write must survive a power cut, and the disk is fast (SSD).
- Even with `always`, you still need **replicas** to survive a disk or machine failure.
- `no-appendfsync-on-rewrite yes` skips fsync during AOF rewrites to avoid latency, but raises the loss window.

<br><br>

## Other Ways to Ask This Question

- How much data can Redis lose with AOF enabled?
- What is the difference between `write()` and `fsync()`?
- Why is `appendfsync always` slow?
- What does "Asynchronous AOF fsync is taking too long" mean?
- How do you make Redis more durable without killing performance?
