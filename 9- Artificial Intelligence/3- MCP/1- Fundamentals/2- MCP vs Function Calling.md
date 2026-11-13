# MCP vs Function Calling

## Question

Why do we need MCP if we can already connect tools directly to an AI agent with function calling?

## Answer

<mark>Function calling is how the model asks for a tool. MCP is how the application finds, connects to and runs that tool. They work together.</mark>

Even with MCP, the LLM still emits a function call. MCP only changes where the tool lives and how the app talks to it.

<br><br>

### Function Calling

- The app defines functions (name, description, JSON schema) and sends them with the prompt.
- The model replies with a structured call like `get_weather({"city": "Lahore"})`.
- The **app's own code** runs the function and sends the result back.
- Tools are hard-coded inside that one app.
- Schema format differs per provider (OpenAI, Anthropic, Gemini).

<br><br>

### MCP

- Tools live in a **separate MCP server**, outside the app.
- The app discovers them at runtime with `tools/list`, so new tools show up without a redeploy.
- The app runs them with `tools/call` through a standard protocol.
- Any MCP-compatible app can reuse the same server.

<br><br>

### Why MCP Helps

- **Reuse:** one GitHub MCP server works in Claude Desktop, Cursor, VS Code and your own agent.
- **Separation of concerns:** the server owns the external API. When GitHub changes its API, you update the server once and every client keeps working.
- **Runtime discovery:** the app doesn't need to know the tool list at build time.
- **Isolation:** credentials and side effects stay in the server process, behind its own auth.
- **Fewer integrations:** M apps + N tools instead of M x N.

<br><br>

### Side by Side

| Aspect          | Function Calling              | MCP                                  |
| :-------------- | :---------------------------- | :----------------------------------- |
| What it is      | Model capability              | Communication protocol               |
| Where tools live| Inside the app code           | In a separate server                 |
| Discovery       | Hard-coded at build time      | `tools/list` at runtime              |
| Reuse           | One app only                  | Any MCP client                       |
| Vendor format   | Differs per LLM provider      | Same for every client                |
| Best for        | Few tools, owned by one app   | Shared tools, many apps or teams     |

<br><br>

### When Plain Function Calling Is Enough

- A small app with 2 or 3 tools nobody else needs.
- Tools that are tightly tied to the app's own logic.
- Cases where the extra process and network hop isn't worth it.

<br><br>

## Other Ways to Ask This Question

- What is the difference between MCP and function calling?
- Does MCP replace function calling?
- MCP vs tool calling, when would you use each?
- Why not just define tools directly in the agent?
- What advantages does MCP give over custom tool integrations?
- How does MCP reduce integration and maintenance overhead?
