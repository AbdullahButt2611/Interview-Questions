# Why MCP Uses JSON-RPC Instead of REST

## Question

Why does MCP use JSON-RPC instead of REST?

## Answer

<mark>MCP needs action-style calls, a long-lived two-way session, and transports other than HTTP. JSON-RPC gives all three. REST gives none of them out of the box.</mark>

A JSON-RPC message is plain JSON with a method name:

```json
{
  "jsonrpc": "2.0",
  "id": 7,
  "method": "tools/call",
  "params": { "name": "read_file", "arguments": { "path": "notes.txt" } }
}
```

<br><br>

### 1. It Is Action-Driven

- JSON-RPC calls **methods** (verbs): `tools/call`, `resources/read`, `prompts/get`.
- An LLM tool call is also a verb: `read_file`, `create_issue`.
- REST is built around **resources** (nouns) and HTTP methods: `GET /files/42`. Mapping "run this tool" onto that shape is awkward.

<br><br>

### 2. It Is Transport-Agnostic

- JSON-RPC is only a message format, so it runs over anything that carries text.
- MCP uses two transports:
  - **stdio:** the host starts the server as a child process and talks over stdin/stdout. No network, no ports.
  - **Streamable HTTP:** for remote servers, with optional SSE streaming. (It replaced the older HTTP+SSE transport.)
- REST depends on HTTP, so it can't talk to a local process over stdio.

<br><br>

### 3. It Is Bidirectional

- In REST, only the client starts a request.
- In MCP, **both sides** send requests and notifications over the same session:
  - Server to client: `sampling/createMessage` (ask the host's LLM), `elicitation/create` (ask the user).
  - Notifications: `notifications/tools/list_changed`, progress updates, logs.

<br><br>

### 4. It Is Stateful

- An MCP session starts with an `initialize` handshake where both sides agree on protocol version and capabilities.
- That state lasts for the whole session. REST is stateless by design.

<br><br>

### Side by Side

| Aspect        | JSON-RPC (MCP)                 | REST                          |
| :------------ | :----------------------------- | :---------------------------- |
| Model         | Methods (actions)              | Resources (nouns)             |
| Transport     | stdio, HTTP, anything          | HTTP only                     |
| Direction     | Both sides send requests       | Client to server only         |
| State         | Session with handshake         | Stateless                     |
| Notifications | Built in                       | Needs webhooks or polling     |

MCP borrowed this design from the **Language Server Protocol (LSP)**, which uses JSON-RPC between code editors and language servers.

<br><br>

## Other Ways to Ask This Question

- Why is MCP built on JSON-RPC 2.0?
- Why didn't MCP use a REST API or gRPC?
- What transports does MCP support?
- What is the difference between stdio and Streamable HTTP in MCP?
- How does an MCP server send messages back to the client?
- Is MCP stateful or stateless?
