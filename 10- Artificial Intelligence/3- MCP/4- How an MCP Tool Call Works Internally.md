# How an MCP Tool Call Works Internally

## Question

How does an MCP tool call work internally, from the user's request to the final answer?

## Answer

<mark>The model picks the tool, the client handles the protocol, and the server runs the operation.</mark>

<br><br>

### Step by Step

1. **Connect and initialize:** the client sends `initialize` with its protocol version and capabilities. The server replies with its own. The client then sends `notifications/initialized`.
2. **Discover tools:** the client calls `tools/list`. The server returns each tool's name, description and JSON input schema.
3. **Give tools to the LLM:** the host converts those schemas into the LLM's function-calling format and sends them with the user's message.
4. **Model picks a tool:** the LLM replies with a tool call, for example `get_weather({"city": "Lahore"})`. It doesn't run anything itself.
5. **Approve (optional):** many hosts ask the user to approve the call before it runs.
6. **Client sends the request:** the host routes the call to the right client, which sends `tools/call` to the server.
7. **Server executes:** the server calls the real API or database and returns the result as `content`. On failure it sets `isError: true`.
8. **Model continues:** the host adds the result to the conversation. The LLM either calls another tool or writes the final answer.

<br><br>

### Flow

```ini
User   -> Host        : "What's the weather in Lahore?"
Host   -> LLM         : user message + tool schemas
LLM    -> Host        : tool call get_weather(city="Lahore")
Host   -> MCP Client  : route call
Client -> MCP Server  : tools/call
Server -> Weather API : GET forecast
Server -> Client      : result { "temp": 31, "sky": "clear" }
Host   -> LLM         : tool result
LLM    -> User        : "It's 31°C and clear in Lahore."
```

<br><br>

### The Messages

```json
// Request (client to server)
{
  "jsonrpc": "2.0", "id": 3, "method": "tools/call",
  "params": { "name": "get_weather", "arguments": { "city": "Lahore" } }
}

// Response (server to client)
{
  "jsonrpc": "2.0", "id": 3,
  "result": {
    "content": [{ "type": "text", "text": "31°C, clear" }],
    "isError": false
  }
}
```

<br><br>

### Who Does What

| Part       | Role                                                       |
| :--------- | :--------------------------------------------------------- |
| LLM        | Decides which tool to call and with what arguments         |
| Host       | Runs the loop, shows approvals, passes results to the LLM  |
| MCP Client | Speaks JSON-RPC to one server                              |
| MCP Server | Validates input, runs the operation, returns the result    |

<br><br>

### Key Points

- Discovery happens once per session, not before every call.
- If the server sends `notifications/tools/list_changed`, the client calls `tools/list` again.
- A tool error goes back to the LLM as a result with `isError: true`, so the model can retry or explain it. Protocol errors (bad method, bad params) use a JSON-RPC `error` object instead.

<br><br>

## Other Ways to Ask This Question

- Walk me through the lifecycle of an MCP tool call.
- What happens between the LLM deciding to call a tool and getting the result?
- What is the MCP initialization handshake?
- How does an MCP client discover available tools?
- Does the LLM execute MCP tools directly?
- How are errors handled in an MCP tool call?
