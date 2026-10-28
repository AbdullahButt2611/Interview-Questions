# MONGO_INITDB_DATABASE

## Question

`MONGO_INITDB_DATABASE: chai_aur_redis` is set. Does the database exist right after the container starts?

```yaml
mongo:
  image: mongo:latest
  environment:
    MONGO_INITDB_DATABASE: chai_aur_redis
  volumes:
    - mongo-data:/data/db
```

## Answer

<mark>No. MongoDB creates a database only on its first write. MONGO_INITDB_DATABASE does not create anything by itself. It only picks which database the init scripts run against.</mark>

```bash
docker exec -it chai_aur_mongo mongosh --eval "show dbs"
# admin, config, local     <- no chai_aur_redis yet
```

<br><br>

### Databases Are Created Lazily

- `use chai_aur_redis` or connecting to `mongodb://.../chai_aur_redis` only **selects** a name.
- The database appears once a **collection** is created, usually by the first insert.

```js
db.users.insertOne({ name: "Ali" });   // now chai_aur_redis exists
```

<br><br>

### What MONGO_INITDB_DATABASE Actually Does

- Sets the database for scripts in `/docker-entrypoint-initdb.d/` (`.js` and `.sh` files).
- In this compose file there are **no init scripts**, so the variable has **no effect**.

<br><br>

### When Init Scripts Run

```ini
Container starts
  -> /data/db empty?          No  -> skip all init, just start mongod
                              Yes -> run scripts in /docker-entrypoint-initdb.d/
                                     against MONGO_INITDB_DATABASE
```

- Only on the **first** start, with an empty data folder.
- Because `mongo-data` persists `/data/db`, scripts **never run again** after the first time. To rerun: `docker compose down -v`.

<br><br>

### How to Actually Create It at Startup

```js
// ./mongo-init/init.js
db.createCollection("users");          // db is already chai_aur_redis
```

```yaml
volumes:
  - mongo-data:/data/db
  - ./mongo-init:/docker-entrypoint-initdb.d:ro
```

<br><br>

### In This Project

- `/mongo` replies `database: "chai_aur_redis"`. That name comes from the **connection string**, not from Mongo.
- The database only appears once the app **writes** something.
- In practice this is fine. Apps do not need to pre-create databases.

<br><br>

### Key Points

- MongoDB databases and collections are created **on first write**.
- `MONGO_INITDB_DATABASE` = target for init scripts, **not** a "create database" switch.
- Init scripts run **once**, only when the data folder is empty.
- `MONGO_INITDB_ROOT_USERNAME` creates the user in `admin`, not in your app database.

<br><br>

## Other Ways to Ask This Question

- When does MongoDB create a database?
- Why does `show dbs` not list my database?
- Why are my scripts in `/docker-entrypoint-initdb.d` not running?
- How do you seed a MongoDB container with data on startup?
- What does `MONGO_INITDB_DATABASE` do in the official Mongo image?
