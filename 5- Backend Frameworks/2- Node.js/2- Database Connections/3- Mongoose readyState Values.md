# Mongoose readyState Values

## Question

What are Mongoose's `readyState` values?

## Answer

<mark>0 = disconnected, 1 = connected, 2 = connecting, 3 = disconnecting (99 = uninitialized).</mark>

```js
mongoose.connection.readyState   // number
```

<br><br>

### The Values

| Value | State         | Meaning                                           |
| :---- | :------------ | :------------------------------------------------ |
| 0     | disconnected  | Not connected (default before `connect()`)        |
| 1     | connected     | Ready, queries run immediately                    |
| 2     | connecting    | `connect()` called, handshake still in progress   |
| 3     | disconnecting | `disconnect()` / `close()` called, shutting down  |
| 99    | uninitialized | Connection object created but never set up (rare) |

<br><br>

### Lifecycle

```ini
0 disconnected --connect()--> 2 connecting --success--> 1 connected
1 connected --disconnect()--> 3 disconnecting --> 0 disconnected
1 connected --network drop--> 0 disconnected --driver retries--> 1 connected
```

<br><br>

### Use Named Constants, Not Magic Numbers

```js
import mongoose from "mongoose";

const { connected } = mongoose.ConnectionStates;   // 1

if (mongoose.connection.readyState === connected) {
  // safe to use mongoose.connection.db
}
```

<br><br>

### Listen to Events Instead of Polling

```js
mongoose.connection.on("connected", () => console.log("Mongo connected"));
mongoose.connection.on("disconnected", () => console.log("Mongo disconnected"));
mongoose.connection.on("reconnected", () => console.log("Mongo reconnected"));
mongoose.connection.on("error", (err) => console.error("Mongo error:", err));
```

<br><br>

### Common Mistakes

- Checking `readyState === 0` and treating everything else as connected. **2 (connecting)** is not ready.
- Using `readyState` as a health check. It is the **driver's view**, not a live test. A dead server can still show `1` for a few seconds.
- For a real health check, ping the server:

```js
await mongoose.connection.db.admin().ping();
```

<br><br>

### Key Points

- Only **1** means ready.
- Some tutorials swap the values of 1 and 2. Correct order: **1 connected, 2 connecting**.
- Prefer `mongoose.ConnectionStates` and connection **events** over raw numbers.

<br><br>

## Other Ways to Ask This Question

- How do you check if Mongoose is connected?
- What does `readyState === 2` mean?
- How do you know when Mongoose reconnects after a network drop?
- Is `readyState` a good health check? Why not?
- Which events does a Mongoose connection emit?
