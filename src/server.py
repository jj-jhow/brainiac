from mcp.server.fastmcp import FastMCP
from src.tools.jira import get_jira_ticket
from src.tools.confluence import search_docs
from src.tools.github import get_pr_context
from src.tools.knowledge import search_knowledge_base

# Initialize MCP Server
mcp = FastMCP("Brainiac")

# Add tools
mcp.add_tool(get_jira_ticket)
mcp.add_tool(search_docs)
mcp.add_tool(get_pr_context)
mcp.add_tool(search_knowledge_base)

if __name__ == "__main__":
    import uvicorn

    # Create the SSE application
    # Note: FastMCP.sse_app is a method that returns a Starlette app
    # We must bind to 0.0.0.0 to expose the server outside the container
    app = mcp.sse_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)
