# Redis vs MongoDB

## Question

Redis vs MongoDB: when do you use each?

## Answer

<mark>Use Redis for fast, temporary, hot data (cache, sessions, rate limits, queues). Use MongoDB as the primary, durable store for your application's documents.</mark>

- They are **not competitors**. Most apps use **both**: Redis in front, MongoDB behind.

<br><br>

### Comparison

| Aspect      | Redis                                  | MongoDB                                    |
| :---------- | :------------------------------------- | :----------------------------------------- |
| Type        | In-memory key-value store              | Disk-based document database               |
| Storage     | RAM (optional RDB / AOF to disk)       | Disk, with a RAM cache for hot pages       |
| Speed       | Sub-millisecond                        | Milliseconds                               |
| Data size   | Limited by RAM                         | Can be much larger than RAM                |
| Data model  | Keys with Strings, Hashes, Lists, Sets | JSON-like documents (BSON)                 |
| Queries     | By key only, no ad-hoc queries         | Rich queries, indexes, aggregation         |
| Durability  | Can lose recent writes (e.g. ~1 sec)   | Durable by default (journal, replica sets) |
| Cost per GB | High (RAM)                             | Low (disk)                                 |

<br><br>

### Use Redis For

- **Caching** query results or API responses.
- **Sessions** and login tokens (with TTL).
- **Rate limiting** (`INCR` + `EXPIRE`).
- **Leaderboards** and rankings (Sorted Sets).
- **Queues**, Pub/Sub, real-time counters.
- Anything where losing it is **OK** because it can be rebuilt.

<br><br>

### Use MongoDB For

- **Primary data**: users, orders, products, posts.
- Data that **must not be lost**.
- **Flexible schema** documents with nested fields.
- **Queries** by any field, filters, sorting, aggregation pipelines.
- Data **larger than RAM**.

<br><br>

### Using Both (Cache-Aside)

```ini
1. App reads key from Redis
2. Hit  -> return it (fast)
3. Miss -> read from MongoDB, store in Redis with a TTL, return it
4. On update -> write to MongoDB, then delete the Redis key
```

- MongoDB stays the **source of truth**.
- Redis cuts read latency and **takes load off** MongoDB.

<br><br>

### Key Points

- Redis = **speed**, MongoDB = **storage and querying**.
- Never keep the only copy of important data in a Redis cache.
- MongoDB's own RAM cache holds data pages, not your computed results. That is why Redis still helps.
- Small app, low traffic: MongoDB alone may be enough. Add Redis when reads get slow or DB load grows.

<br><br>

## Other Ways to Ask This Question

- Why use Redis if you already have MongoDB?
- Can Redis be used as a primary database?
- When would you add a cache in front of your database?
- What is the cache-aside pattern?
- In-memory database vs disk-based database: trade-offs?
- Where would you store sessions: Redis or MongoDB? Why?
