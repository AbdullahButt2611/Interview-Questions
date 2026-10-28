# Core Redis Data Types

## Question

Name the core Redis data types.

## Answer

<mark>Core types: String, List, Hash, Set, Sorted Set, Stream. Special types: Bitmap, HyperLogLog, Geospatial.</mark>

- Every key holds **one** type. Check it with `TYPE key`.

<br><br>

### Core Types

| Type       | What it is                          | Example commands              | Use case                     |
| :--------- | :---------------------------------- | :---------------------------- | :--------------------------- |
| String     | Bytes: text, number, JSON (≤ 512MB) | `SET`, `GET`, `INCR`          | Cache, counters, sessions    |
| List       | Ordered by insertion, duplicates OK | `LPUSH`, `RPOP`, `LRANGE`     | Queues, stacks, recent items |
| Hash       | Field-value pairs under one key     | `HSET`, `HGET`, `HGETALL`     | Objects (user profile)       |
| Set        | Unique, unordered strings           | `SADD`, `SISMEMBER`, `SINTER` | Tags, unique visitors        |
| Sorted Set | Unique strings ordered by a score   | `ZADD`, `ZRANGE`, `ZRANK`     | Leaderboards, rate limits    |
| Stream     | Append-only log of entries          | `XADD`, `XREAD`, `XACK`       | Event logs, message queues   |

<br><br>

### Special Types

| Type        | Built on   | Example commands        | Use case                          |
| :---------- | :--------- | :---------------------- | :-------------------------------- |
| Bitmap      | String     | `SETBIT`, `BITCOUNT`    | Daily active users, feature flags |
| HyperLogLog | String     | `PFADD`, `PFCOUNT`      | Approx unique counts, ~12KB fixed |
| Geospatial  | Sorted Set | `GEOADD`, `GEOSEARCH`   | Nearby stores, distance queries   |

<br><br>

### Quick Examples

```bash
SET page:views 0          # String
INCR page:views

LPUSH jobs "email:42"     # List as a queue
RPOP jobs

HSET user:1 name "Ali" age 25   # Hash
HGET user:1 name

SADD post:1:tags redis docker   # Set

ZADD leaderboard 150 "ali" 90 "sara"   # Sorted Set
ZREVRANGE leaderboard 0 9 WITHSCORES   # top 10

XADD orders * id 101 status "paid"     # Stream
```

<br><br>

### Picking the Right Type

- Need a simple value or counter: **String**
- Need order of arrival: **List**
- Need an object with fields: **Hash** (update one field without rewriting all)
- Need uniqueness: **Set**
- Need ranking or sorting by a number: **Sorted Set**
- Need a durable queue with consumer groups and ACKs: **Stream**

<br><br>

### Key Points

- Redis is a **data structure server**, not just a string cache.
- Bitmap and HyperLogLog are **strings** under the hood. Geospatial is a **sorted set**.
- Small Lists, Hashes, Sets and Sorted Sets use **compact encodings** (listpack, intset) to save memory.
- Redis 8 also ships JSON, Time Series, probabilistic types (Bloom filter) and Vector Sets.

<br><br>

## Other Ways to Ask This Question

- What data structures does Redis support?
- Which Redis type would you use for a leaderboard? Why?
- Hash vs storing JSON in a String: which is better for objects?
- List vs Stream for a message queue?
- How do you count unique visitors in Redis with very little memory?
- What is the difference between a Set and a Sorted Set?
