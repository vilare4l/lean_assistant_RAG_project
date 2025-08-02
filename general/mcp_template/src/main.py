from mcp.server.fastmcp import FastMCP, Context
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
from dotenv import load_dotenv
import asyncio
import os

from tools.example_tool import perform_example_operation

# Load environment variables from .env file
load_dotenv()

# Define a simple context for your MCP server if needed
@dataclass
class MyMCPContext:
    """Context for this MCP server."""
    # Add any resources your MCP needs to initialize once at startup
    # For example: database_client: Any
    pass

@asynccontextmanager
async def mcp_lifespan(server: FastMCP) -> AsyncIterator[MyMCPContext]:
    """
    Manages the lifecycle of resources for this MCP server.
    Initialize resources here before the server starts.
    """
    # Example: Initialize a database client or an external API client
    # my_resource = initialize_my_resource()
    
    try:
        yield MyMCPContext() # Pass initialized resources here if any
    finally:
        # Clean up resources here when the server shuts down
        # Example: await my_resource.close()
        pass

# Initialize FastMCP server
mcp = FastMCP(
    "mcp-template", # Unique name for your MCP
    description="A template MCP server demonstrating modular tool implementation.",
    lifespan=mcp_lifespan,
    host=os.getenv("HOST", "0.0.0.0"),
    port=os.getenv("PORT", "8050")
)        

# Example MCP Tool 1: Basic greeting
@mcp.tool()
async def greet_user(ctx: Context, name: str) -> str:
    """
    Greets the user with a personalized message.
    
    Args:
        ctx: The MCP server provided context.
        name: The name of the user to greet.
    """
    return f"Hello, {name}! Welcome to your custom MCP."

# Example MCP Tool 2: Process generic data, delegating to an external tool file
@mcp.tool()
async def process_generic_data(ctx: Context, input_data: str) -> str:
    """
    Processes generic input data using a delegated function from the tools directory.

    Args:
        ctx: The MCP server provided context.
        input_data: The data string to be processed.
    """
    try:
        processed_result = perform_example_operation(input_data)
        return f"Data processed successfully: {processed_result}"
    except Exception as e:
        return f"Error processing data: {str(e)}"

# Main function to run the MCP server
async def main():
    transport = os.getenv("TRANSPORT", "sse")
    if transport == 'sse':
        # Run the MCP server with SSE transport (HTTP endpoint)
        print(f"Starting MCP server with SSE on http://{os.getenv('HOST', '0.0.0.0')}:{os.getenv('PORT', '8050')}/sse")
        await mcp.run_sse_async()
    else:
        # Run the MCP server with Stdio transport (CLI-based)
        print("Starting MCP server with Stdio transport.")
        await mcp.run_stdio_async()

if __name__ == "__main__":
    asyncio.run(main())