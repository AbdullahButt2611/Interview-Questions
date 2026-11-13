# Cold Start Race Condition

## Question

**Race condition:** two requests hit `/mongo` at the same moment on a cold start. What happens?

```js
app.get("/mongo", async (req, res) => {
  if (mongoose.connection.readyState === 0) {
    await mongoose.connect(url);
  }
  res.json({ mongo: "Connected", database: mongoose.connection.name });
});
```

## Answer

<mark>Request A starts connecting. Request B sees "connecting" (not 0), skips the await, and replies "Connected" before the connection is actually ready.</mark>

<br><br>

### readyState Values

```ini
0 = disconnected
1 = connected
2 = connecting
3 = disconnecting
```

- The code only checks for `0`. State `2` slips through as if it were connected.

<br><br>

### Step by Step

```ini
t0  A: readyState = 0  -> calls mongoose.connect()  -> readyState = 2
t1  A: awaits (connection in progress)
t2  B: readyState = 2  -> condition false, skips connect
t3  B: responds { mongo: "Connected" }        <- LIE, not connected yet
t4  A: connect resolves -> readyState = 1 -> responds "Connected"
```

- `await` gives up the event loop, so B runs while A is still waiting.
- Node is single-threaded, but **async code still races** at every `await`.

<br><br>

### What Can Go Wrong

- **False health report:** B says "Connected" even if A's connect later **fails**.
- **Crash on raw access:** if B used `mongoose.connection.db.admin().ping()`, it throws `TypeError` because `db` is not set yet.
- **Hidden delay:** model queries (`User.find()`) in B do not fail. Mongoose **buffers** them until connected (default 10s timeout), which hides the bug.
- **Double connect:** with slightly different timing, both requests can see `0` and both call `connect()`.

<br><br>

### Fix 1: Connect at Boot (Best)

```js
await mongoose.connect(url);   // before app.listen()
app.listen(3000);
```

- No request can ever see a half-open connection.

<br><br>

### Fix 2: Cache the Connect Promise (If Lazy Is Needed)

```js
let mongoReady = null;

function connectMongo() {
  mongoReady ??= mongoose.connect(url).catch((err) => {
    mongoReady = null;   // allow a retry next time
    throw err;
  });
  return mongoReady;
}

app.get("/mongo", async (req, res) => {
  await connectMongo();   // A and B await the SAME promise
  res.json({ mongo: "Connected", database: mongoose.connection.name });
});
```

- Every request waits on **one shared promise**. Nobody skips ahead.
- Clearing it on failure stops a single failed attempt from being cached forever.

<br><br>

### Key Points

- "Check then act" across an `await` is a classic **race**: the state can change between the check and the action.
- Cache the **promise**, not a boolean flag. A flag set after `connect` resolves has the same gap.
- A health endpoint should **actually ping** the DB, not just read a state flag.

<br><br>

## Other Ways to Ask This Question

- Can race conditions happen in single-threaded Node.js? How?
- What are Mongoose's `readyState` values?
- Why does caching a promise prevent duplicate connections?
- Why does `mongoose.connection.db` sometimes come back `undefined`?
- How do you make a lazy-initialized resource safe under concurrent requests?
- What is the "check then act" problem?
