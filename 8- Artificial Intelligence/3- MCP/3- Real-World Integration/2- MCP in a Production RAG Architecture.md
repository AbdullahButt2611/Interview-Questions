# MCP in a Production RAG Architecture

## Question

How does MCP fit into a production RAG (Retrieval-Augmented Generation) architecture, for example on Google Cloud?

## Answer

<mark>MCP is the doorway the agent uses to reach the retrieval service. It does not do embeddings, vector search or reranking, and a RAG system can work without it.</mark>

<br><br>

### Architecture on Google Cloud

```ini
User
 -> ADK Agent (Gemini)
 -> McpToolset
 -> MCP Server: search_docs(query, filters)
 -> Retrieval API (Cloud Run)
      1. embed query        (Vertex AI embeddings)
      2. vector / hybrid search (Vertex AI Vector Search)
      3. metadata filter    (tenant, date, doc type)
      4. rerank top-k       (Vertex AI Ranking API)
 -> top chunks + source links
 -> ADK Agent -> Gemini writes a grounded answer with citations
```

<br><br>

### Who Does What

| Layer             | Job                                                         |
| :---------------- | :---------------------------------------------------------- |
| ADK Agent / LLM   | Decides when to search, writes the final answer             |
| MCP Server        | Exposes `search_docs` as a tool, checks auth, formats output |
| Retrieval API     | Embeds the query, searches, filters, reranks                |
| Vector Search     | Stores embeddings and finds nearest neighbours              |
| Ingestion pipeline| Chunks documents, embeds them, writes to the index (offline) |

<br><br>

### What MCP Adds

- **Agentic retrieval:** the model calls `search_docs` only when it needs to, and can search again with a better query. Classic RAG retrieves once before every answer.
- **Reuse:** the same retrieval server works for the support bot, the internal Slack agent and an IDE assistant.
- **One place for access control:** the server applies per-user or per-tenant filters, so one agent can't read another team's documents.
- **Swap the backend freely:** move from Vector Search to AlloyDB pgvector or Vertex AI RAG Engine without touching the agent.
- **Resources:** the server can also expose documents as MCP resources for the app to attach directly.

<br><br>

### What MCP Does Not Do

- Chunking or embedding documents.
- Vector or keyword search.
- Reranking or answer generation.
- Guaranteeing the answer is grounded. That still depends on retrieval quality and the prompt.

<br><br>

### When to Skip MCP

- One app, one retrieval step, one team. Calling the retrieval API directly from the agent (or using a built-in Vertex AI RAG tool) is simpler.
- Very latency-sensitive paths, where the extra hop matters.

<br><br>

## Other Ways to Ask This Question

- Where does MCP sit in a RAG pipeline?
- Can you build RAG using MCP? How?
- Does MCP replace a vector database?
- Design a RAG system on Google Cloud using ADK and MCP.
- What is the difference between classic RAG and agentic RAG with MCP tools?
- Is MCP required for RAG?
