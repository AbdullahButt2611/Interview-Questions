# Integrating MCP with Google ADK

## Question

How do you integrate an MCP server with an agent built on Google ADK (Agent Development Kit)?

## Answer

<mark>Use `McpToolset`. It connects to an MCP server, lists its tools, and hands them to the ADK agent as regular tools.</mark>

```ini
ADK Agent -> McpToolset (MCP client) -> MCP Server -> External API
```

The agent can then use remote tools without you writing each integration as a local Python function.

<br><br>

### Steps

1. Pick how to connect to the server:
   - `StdioConnectionParams` for a local server started as a subprocess.
   - `StreamableHTTPConnectionParams` for a remote server.
   - `SseConnectionParams` for older servers that still use SSE.
2. Create an `McpToolset` with those params.
3. Optionally limit tools with `tool_filter`.
4. Pass the toolset in the agent's `tools` list.
5. Close the toolset when the app shuts down so the connection and subprocess are cleaned up.

<br><br>

### Example (Local File System Server)

```python
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams
from mcp import StdioServerParameters

files_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem", "/data/docs"],
        ),
    ),
    tool_filter=["read_file", "list_directory"],  # only expose these
)

root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="docs_agent",
    instruction="Answer questions using the files in /data/docs.",
    tools=[files_toolset],
)
```

<br><br>

### Example (Remote Server)

```python
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams

remote_toolset = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="https://mcp.example.com/mcp",
        headers={"Authorization": "Bearer <token>"},
    ),
)
```

<br><br>

### Two Directions

- **ADK as MCP client:** the agent uses tools from an MCP server (the examples above).
- **ADK as MCP server:** you wrap ADK tools in an MCP server so other hosts (Claude Desktop, Cursor) can call them. ADK has a helper to convert ADK tools to MCP tool schemas for this.

<br><br>

### Production Notes

- Use `tool_filter` to expose only the tools the agent needs. Fewer tools means better tool selection and a smaller blast radius.
- Keep secrets in the server or in headers from a secret manager, not in the prompt.
- On Cloud Run or Agent Engine, prefer a remote server over stdio, since spawning `npx` inside the container adds cold-start time.

<br><br>

## Other Ways to Ask This Question

- How do you connect a Google ADK agent to an MCP server?
- What is `McpToolset` in Google ADK?
- How do you use stdio vs remote MCP servers in ADK?
- Can an ADK agent expose its own tools as an MCP server?
- How do you restrict which MCP tools an ADK agent can use?
- How would you add third-party tools to a Gemini agent without writing custom functions?
