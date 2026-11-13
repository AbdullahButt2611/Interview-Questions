# Cache Invalidation

## Question

How do you invalidate a cache entry when the Mongo document changes?

## Answer

<mark>Write to Mongo first, then delete the Redis key. The next read misses the cache and reloads the fresh document. Always keep a TTL as a safety net.</mark>

```js
async function updateUser(id, data) {
  const user = await User.findByIdAndUpdate(id, data, { new: true });   // 1. DB first
  await redis.del(`user:${id}`);                                        // 2. then delete
  return user;
}
```

<br><br>

### Why Delete, Not Update the Cache

- **Race-safe:** two writers updating the cache at once can leave the **older** value last. A delete cannot be "out of order".
- **Simple:** the read path already knows how to rebuild the entry.
- **Cheap:** no work spent caching a value that may never be read.

<br><br>

### Why DB First, Then Delete

```ini
Wrong order: delete -> update DB
  t1  writer deletes user:1
  t2  reader misses, reads OLD doc from Mongo, caches it
  t3  writer updates Mongo           -> cache is stale until TTL

Right order: update DB -> delete
  t1  writer updates Mongo
  t2  writer deletes user:1
  t3  reader misses, reads NEW doc   -> correct
```

- A tiny race remains (a slow reader can cache an old value just after the delete). A **TTL** caps how long that lasts.

<br><br>

### Common Problems and Fixes

| Problem                                         | Fix                                                      |
| :---------------------------------------------- | :------------------------------------------------------- |
| `DEL` fails (Redis down)                        | TTL on every key, so stale data expires anyway           |
| One document affects many keys (lists, counts)  | Track keys per document in a Set, or use versioned keys  |
| Other services or scripts update Mongo directly | Use **MongoDB change streams** to delete keys            |
| `updateMany` skips your invalidation code       | Invalidate in a shared function, not scattered in routes |

<br><br>

### Invalidate Many Keys: Versioned Keys

```js
// read
const v = (await redis.get(`user:${id}:v`)) ?? 0;
const key = `user:${id}:profile:v${v}`;

// on update
await redis.incr(`user:${id}:v`);   // old keys are never read again, TTL cleans them up
```

<br><br>

### Catch Every Change: Change Streams

```js
User.watch().on("change", (change) => {
  redis.del(`user:${change.documentKey._id}`).catch(console.error);
});
```

- Fires for **any** write to the collection, from any app or script.
- Requires a MongoDB **replica set** (works on a single-node replica set too).

<br><br>

### Key Points

- Pattern: **update DB, then delete the key** (cache-aside).
- Delete instead of update, to avoid race conditions.
- **TTL on every cache key.** It limits the damage of any missed invalidation.
- For writes outside your app, use change streams.

<br><br>

## Other Ways to Ask This Question

- How do you keep Redis and MongoDB in sync?
- Should you update or delete the cache when data changes?
- Why do you write to the database before deleting the cache key?
- How do you invalidate a cached list when one item in it changes?
- What are MongoDB change streams used for?
- What happens if the cache delete fails?
