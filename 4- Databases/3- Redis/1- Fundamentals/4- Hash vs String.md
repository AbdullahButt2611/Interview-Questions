# Redis Hash vs String

## Question

What is a Redis Hash, and when would you use one instead of a String?

## Answer

<mark>A Hash is a map of field-value pairs stored under one key, like a small flat object. Use a Hash when you read or update individual fields. Use a String (with JSON) when you always read and write the whole object, or the data is nested.</mark>

<br><br>

### Same Object, Two Ways

```bash
# Hash: one key, many fields
HSET user:1 name "Ali" age 25 city "Lahore"
HGET user:1 name               # "Ali"
HINCRBY user:1 age 1           # 26, updates one field atomically

# String: whole object as JSON
SET user:1 '{"name":"Ali","age":25,"city":"Lahore"}'
GET user:1                     # full JSON, parse in the app
```

```js
// ioredis
await redis.hset("user:1", { name: "Ali", age: 25 });
const user = await redis.hgetall("user:1");   // { name: "Ali", age: "25" }  values are strings
```

<br><br>

### Comparison

| Aspect                        | Hash                                            | String (JSON)                        |
| :---------------------------- | :---------------------------------------------- | :----------------------------------- |
| Read one field                | `HGET`, cheap                                   | `GET` all, parse, pick one           |
| Update one field              | `HSET` / `HINCRBY`, **atomic**                  | Read, modify, write back (race risk) |
| Read whole object             | `HGETALL`                                       | `GET` + `JSON.parse`, one call       |
| Nested data (arrays, objects) | **No**, flat only                               | **Yes**                              |
| Value types                   | Always strings                                  | JSON keeps numbers, booleans         |
| TTL                           | Whole key, or per field (Redis 7.4+, `HEXPIRE`) | Whole key only                       |
| Memory                        | Small hashes use compact listpack encoding      | About the same per object            |

<br><br>

### Use a Hash When

- You **update single fields** often: counters, status, last-seen time.
- Several clients may write **different fields at the same time** (no lost updates).
- You read **a few fields**, not the whole object (`HMGET user:1 name city`).
- You have **many tiny values**: fields in one Hash use less memory than thousands of separate keys (each key has its own overhead).

<br><br>

### Use a String When

- You cache a **whole Mongo document or API response** and always read it in full.
- The data is **nested** (arrays, sub-objects).
- You want types preserved after a round trip.

<br><br>

### The Lost-Update Problem with Strings

```ini
Client A: GET user:1 -> age 25, change city -> SET (age 25, city Karachi)
Client B: GET user:1 -> age 25, add 1 to age -> SET (age 26, city Lahore)
Last write wins: one change is lost

Hash:     HSET user:1 city Karachi  +  HINCRBY user:1 age 1   -> both kept
```

<br><br>

### Key Points

- Hash = **flat object** with field-level reads, writes and atomic increments.
- String + JSON = **whole-object** cache, supports nesting.
- For cache-aside of Mongo documents, a **JSON String** is usually simplest.
- Need nested **and** partial updates? Use **RedisJSON** (`JSON.SET user:1 $.age 26`), built into Redis 8.

<br><br>

## Other Ways to Ask This Question

- How do you store objects in Redis?
- Should you serialize a Mongo document into a Redis JSON string or a Hash?
- What does `HINCRBY` do, and why is it safer than GET then SET?
- Why does `HGETALL` return numbers as strings?
- Can you set a TTL on a single field of a Redis Hash?
- What is RedisJSON?
