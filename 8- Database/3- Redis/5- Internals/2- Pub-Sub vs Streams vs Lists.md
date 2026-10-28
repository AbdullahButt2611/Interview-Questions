# Pub/Sub vs Streams vs Lists

## Question

Is Redis a reliable message queue? Pub/Sub vs Streams vs Lists.

## Answer

<mark>It depends on the structure. Pub/Sub is fire-and-forget (messages lost if nobody is listening). Lists are a simple queue but lose a message if the worker crashes after popping it. Streams are the reliable option: persisted, with consumer groups, acknowledgements and redelivery.</mark>

- Even Streams are only as durable as Redis persistence (AOF `everysec` can lose ~1 second).

<br><br>

### Comparison

| Feature                | Pub/Sub                                      | Lists                     | Streams                          |
| :--------------------- | :------------------------------------------- | :------------------------ | :------------------------------- |
| Stored in Redis        | **No**                                       | Yes                       | Yes                              |
| Offline consumer       | Misses messages                              | Picks up later            | Picks up later                   |
| Delivery               | At most once                                 | At most once (by default) | **At least once**                |
| Acknowledgement        | No                                           | Manual pattern only       | **Built in** (`XACK`)            |
| Crash after receiving  | Lost                                         | Lost (unless `BLMOVE`)    | Stays pending, redelivered       |
| Fan-out (many readers) | **Yes**, all subscribers                     | No, one consumer per item | Yes, one per consumer group      |
| Replay old messages    | No                                           | No                        | **Yes**, by ID                   |
| Best for               | Live notifications, chat, cache invalidation | Simple job queues         | Event logs, reliable work queues |

<br><br>

### Pub/Sub: Fire and Forget

```bash
SUBSCRIBE notifications          # client 1
PUBLISH notifications "hello"    # client 2, returns number of receivers
```

- Delivered only to clients **connected right now**. Nobody listening = message gone.
- A slow subscriber gets **disconnected** when its output buffer fills.
- In ioredis, a subscribed connection can only run subscribe commands. Use a **separate client** for normal commands.

<br><br>

### Lists: Simple Queue

```bash
LPUSH jobs '{"id":1}'                          # producer
BRPOP jobs 0                                   # worker blocks until a job arrives
```

- Problem: after `BRPOP`, the job exists **only in the worker's memory**. Worker crashes = job lost.
- Reliable-queue pattern: move it to a processing list, delete only when done:

```bash
BLMOVE jobs processing RIGHT LEFT 0            # atomically pop and keep a copy
LREM processing 1 '{"id":1}'                   # after success
```

- Recovering stuck items from `processing` is **your** code's job.

<br><br>

### Streams: Reliable Log

```bash
XADD orders * id 101 status paid                          # producer
XGROUP CREATE orders workers $ MKSTREAM                   # once
XREADGROUP GROUP workers w1 COUNT 10 BLOCK 5000 STREAMS orders >
XACK orders workers 1700000000000-0                       # after success
XAUTOCLAIM orders workers w2 60000 0                      # take over jobs stuck > 60s
```

- Unacknowledged messages stay in the **Pending Entries List** until `XACK`.
- A crashed worker's messages can be **claimed** by another worker.
- Several consumer groups can each read the full stream (fan-out + work sharing).
- Trim with `MAXLEN` so the stream does not grow forever.

<br><br>

### When Redis Is Not Enough

- Must never lose a message, even on failover: Redis replication is **asynchronous**, so a failover can drop acknowledged writes.
- Huge throughput or long retention (days of events): data must fit in **RAM**.
- Then use **Kafka**, **RabbitMQ** or **SQS**.
- For job queues in Node.js, **BullMQ** builds retries, delays and priorities on top of Redis.

<br><br>

### Key Points

- **Pub/Sub** = broadcast to whoever is online. Not a queue.
- **Lists** = simple queue, needs `BLMOVE` + cleanup to be crash-safe.
- **Streams** = consumer groups, acks, redelivery, replay. The right Redis choice for reliable messaging.
- Reliability still depends on **persistence and replication** settings.

<br><br>

## Other Ways to Ask This Question

- Can Redis replace Kafka or RabbitMQ?
- Why does Redis Pub/Sub lose messages?
- What is a consumer group in Redis Streams?
- How do you build a reliable queue with Redis Lists?
- What happens to a Stream message if the worker crashes before `XACK`?
- At-most-once vs at-least-once delivery: what is the difference?
