# JSON.stringify Before SET

## Question

Why do we call `JSON.stringify` before `SET`?

```js
await redis.set("user:1", JSON.stringify(user), "EX", 3600);
const user = JSON.parse(await redis.get("user:1"));
```

## Answer

<mark>Redis Strings store bytes, not JavaScript objects. ioredis turns every argument into text with String(), so an object becomes "[object Object]" and the data is lost silently. JSON.stringify turns it into real text, and JSON.parse turns it back.</mark>

<br><br>

### What Happens Without It

```js
await redis.set("user:1", { name: "Ali", age: 25 });
await redis.get("user:1");   // "[object Object]"   no error, data gone
```

- ioredis converts arguments with `String(arg)`:

| Value passed to `SET` | Stored as           |
| :-------------------- | :------------------ |
| `{ name: "Ali" }`     | `"[object Object]"` |
| `[1, 2, 3]`           | `"1,2,3"`           |
| `25`                  | `"25"`              |
| `true`                | `"true"`            |
| `null` / `undefined`  | `""` (empty string) |

- Exception: `hset` and `mset` accept an object and spread it into fields. `set` does not.

<br><br>

### The Round Trip

```ini
JS object  --JSON.stringify-->  '{"name":"Ali","age":25}'  --SET-->  Redis
Redis      --GET-->  '{"name":"Ali","age":25}'  --JSON.parse-->  JS object
```

- A cache miss returns `null`. Check it before parsing:

```js
const raw = await redis.get("user:1");
const user = raw ? JSON.parse(raw) : await loadFromMongo(1);
```

<br><br>

### What JSON Does Not Preserve

| Type              | After stringify + parse      |
| :---------------- | :--------------------------- |
| `Date`            | ISO **string**, not a `Date` |
| `undefined` field | Field **removed**            |
| `Map`, `Set`      | `{}` (empty object)          |
| `BigInt`          | **Throws** an error          |
| Mongo `ObjectId`  | Plain string                 |
| Circular object   | **Throws** an error          |

- For Mongoose, cache plain data: `User.findById(id).lean()`, then stringify.

<br><br>

### Alternatives

- **Hash** (`HSET`): flat objects, field-level updates.
- **RedisJSON** (`JSON.SET`): stores real JSON, supports nested paths (Redis 8).
- **MessagePack**: binary format, smaller and faster than JSON, stored as a Buffer.

<br><br>

### Key Points

- Redis values are **strings/bytes**. Serialization is the **client's** job.
- Without `JSON.stringify`, objects become `"[object Object]"` with **no error**.
- `JSON.parse` on read, and handle `null` for cache misses.
- JSON loses Dates, Maps, `undefined` and BigInts. Convert them yourself if needed.

<br><br>

## Other Ways to Ask This Question

- Why does Redis return `[object Object]`?
- How do you store a JavaScript object in Redis?
- What is serialization, and why does a cache need it?
- Why does a Date come back as a string from the cache?
- JSON vs MessagePack for Redis values?
