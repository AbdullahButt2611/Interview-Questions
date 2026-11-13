# What is MCP and What Problem Does It Solve?

## Question

What is MCP (Model Context Protocol), and what problem does it solve?

## Answer

<mark>MCP is an open protocol that standardizes how AI applications connect to external tools, data, and prompts.</mark>

Anthropic released it in November 2024. Claude, ChatGPT, Gemini, VS Code, Cursor and many agent frameworks now support it.

Think of it like:

```ini
USB-C  = one port, any device
MCP    = one protocol, any tool or data source
```

<br><br>

### The Problem Before MCP

- Every AI app wrote its own glue code for every tool (GitHub, Slack, Postgres, Google Drive...).
- 5 apps and 10 tools meant up to **50 custom integrations**, each with its own auth, schema and error handling.
- An integration built for one app could not be reused in another.

```ini
Without MCP:  M apps x N tools  = M x N integrations
With MCP:     M clients + N servers = M + N integrations
```

<br><br>

### Architecture (Client-Server)

- **Host:** the AI application the user talks to (Claude Desktop, an IDE, your agent).
- **Client:** lives inside the host and keeps a 1:1 connection with one MCP server.
- **Server:** a separate program that exposes capabilities from a system (a database, an API, the file system).

```ini
Host (AI app)
  ├── MCP Client 1  <──>  MCP Server: GitHub
  ├── MCP Client 2  <──>  MCP Server: Postgres
  └── MCP Client 3  <──>  MCP Server: File System
```

<br><br>

### What a Server Can Expose

| Primitive     | Controlled by | What it is                                   | Example                         |
| :------------ | :------------ | :------------------------------------------- | :------------------------------ |
| **Tools**     | Model         | Functions the LLM can call                   | `create_issue`, `run_query`     |
| **Resources** | Application   | Read-only data the app attaches as context   | a file, a DB schema, a log      |
| **Prompts**   | User          | Reusable prompt templates                    | "Summarize this PR" slash command |

Clients can also offer features back to the server, such as **sampling** (the server asks the host's LLM for a completion) and **elicitation** (the server asks the user for input).

<br><br>

### Key Points

- MCP is a **protocol**, not a library or a model feature.
- Messages use **JSON-RPC 2.0**.
- Transports: **stdio** for local servers, **Streamable HTTP** for remote ones.
- Build a server once and any MCP-compatible host can use it.

<br><br>

## Other Ways to Ask This Question

- What is the Model Context Protocol?
- Explain MCP in simple terms.
- What are the main components of MCP architecture?
- What is the difference between an MCP host, client and server?
- What are tools, resources and prompts in MCP?
- Why did Anthropic create MCP?
