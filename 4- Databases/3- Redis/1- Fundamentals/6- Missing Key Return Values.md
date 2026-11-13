# Missing Key Return Values

## Question

What does `GET` return for a key that doesn't exist? What does `HGETALL` return?

## Answer

<mark>GET returns nil (null in ioredis). HGETALL returns an empty hash ({} in ioredis), not null. An empty object is truthy in JavaScript, so if (user) wrongly treats a missing hash as found.</mark>

```bash
127.0.0.1:6379> GET nope
(nil)
127.0.0.1:6379> HGETALL nope
(empty array)
```

<br><br>

### The JavaScript Trap

```js
const s = await redis.get("user:99");       // null
const h = await redis.hgetall("user:99");   // {}

if (s) { /* skipped, correct */ }
if (h) { /* RUNS, {} is truthy: bug */ }

// correct check for hashes
if (Object.keys(h).length === 0) {
  // cache miss
}
```

<br><br>

### Missing Key: What Each Command Returns

| Command             | redis-cli        | ioredis        |
| :------------------ | :--------------- | :------------- |
| `GET key`           | `(nil)`          | `null`         |
| `HGET key field`    | `(nil)`          | `null`         |
| `HGETALL key`       | `(empty array)`  | `{}`           |
| `HMGET key a b`     | `(nil)`, `(nil)` | `[null, null]` |
| `MGET k1 k2`        | `(nil)`, `(nil)` | `[null, null]` |
| `LRANGE key 0 -1`   | `(empty array)`  | `[]`           |
| `SMEMBERS key`      | `(empty array)`  | `[]`           |
| `ZSCORE key member` | `(nil)`          | `null`         |
| `EXISTS key`        | `0`              | `0`            |
| `TTL key`           | `-2`             | `-2`           |
| `INCR key`          | `1` (creates it) | `1`            |

<br><br>

### Why Collections Return Empty, Not nil

- In Redis, an **empty** List, Set, Hash or Sorted Set **does not exist**. Removing the last item deletes the key.
- So "missing" and "empty" are the **same thing** for collections, and Redis returns an empty result.
- Strings are different: an empty string `""` is a real value, so a missing String must be `nil`.

<br><br>

### Related Return Codes

| `TTL` result | Meaning                       |
| :----------- | :---------------------------- |
| `-2`         | Key does not exist            |
| `-1`         | Key exists, has **no** expiry |
| `>= 0`       | Seconds until it expires      |

- Wrong type (e.g. `GET` on a Hash) is an **error**, not nil: `WRONGTYPE Operation against a key holding the wrong kind of value`.

<br><br>

### Key Points

- `GET` miss = `null`. Check with `if (value === null)`.
- `HGETALL` miss = `{}`. Check with `Object.keys(obj).length === 0`, or use `EXISTS` first.
- Collections are never "empty but existing". Empty = deleted.
- `TTL -2` = missing, `TTL -1` = no expiry.

<br><br>

## Other Ways to Ask This Question

- How do you check for a cache miss on a Redis Hash in Node.js?
- Why is my code treating a missing Redis hash as found?
- What is the difference between `nil` and an empty array in Redis?
- What do `TTL` return values `-1` and `-2` mean?
- Can a Redis List or Set exist while empty?
- What happens if you `GET` a key that holds a Hash?
