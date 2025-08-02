# MCP Template: A Foundation for Model Context Protocol Servers

This project serves as a robust template for building your own Model Context Protocol (MCP) servers. It incorporates best practices for project structure, dependency management, configuration, and containerization, allowing you to quickly develop and deploy custom MCP functionalities.

## Features

- **Standardized Project Structure**: Clear separation of source code, documentation, and tests.
- **Modular Tool Implementation**: Tools are defined in `src/main.py` and can delegate complex logic to dedicated files in the `tools/` directory.
- **Dependency Management**: Uses `pyproject.toml` and `uv` for efficient dependency handling.
- **Environment Configuration**: Securely manage sensitive information with `.env` files.
- **Containerization**: Ready-to-use `Dockerfile` for easy deployment with Docker.
- **Extensible MCP Server**: A basic `FastMCP` setup ready for you to add your custom tools and resources.

## Getting Started

### Prerequisites

- Python 3.12+
- `uv` (install with `pip install uv` if you don't have it)
- Docker (recommended for deployment)

### Installation

1.  **Clone this template or copy its contents**:
    ```bash
    git clone <your-repo-url> my-mcp-server
    cd my-mcp-server
    ```
    (If you copied, ensure you are in your new project directory)

2.  **Install dependencies**:
    ```bash
    uv pip install -e .
    ```

3.  **Create your environment file**:
    ```bash
    cp .env.example .env
    ```
    Edit the `.env` file to configure your server's transport, host, port, and any other custom variables your MCP might need.

### Running the Server

You can run the MCP server using `uv` directly or via Docker.

#### Using `uv` (for development)

Set `TRANSPORT=sse` in your `.env` file for an HTTP endpoint, or leave it empty for `stdio` (CLI-based) transport.

```bash
uv run src/main.py
```

#### Using Docker (recommended for deployment)

1.  **Build the Docker image**:
    ```bash
    docker build -t my-mcp-server .
    ```

2.  **Run the Docker container**:
    ```bash
    docker run --env-file .env -p 8050:8050 my-mcp-server
    ```
    (Adjust the port mapping `-p 8050:8050` if you configured a different `PORT` in your `.env` file).

## Building Your Custom MCP

This template provides a minimal MCP server. To add your own functionalities:

1.  **Define your MCP Tools in `src/main.py`**:
    Each function decorated with `@mcp.tool()` in `src/main.py` becomes an exposed MCP tool. These tools should represent distinct capabilities your MCP offers.
    Example:
    ```python
    # src/main.py
    from mcp.server.fastmcp import FastMCP, Context

    # ... (your MCP setup)

    @mcp.tool()
    async def my_first_tool(ctx: Context, input_param: str) -> str:
        """A simple tool exposed by the MCP."""
        return f"Processed: {input_param.upper()}"
    ```

2.  **Organize Complex Tool Logic in `tools/`**:
    For tools with complex logic, delegate the implementation to separate Python files within the `tools/` directory. Import these functions into `src/main.py` and call them from your `@mcp.tool()` decorated functions.
    Example (`src/main.py` calling `tools/my_complex_logic.py`):
    ```python
    # src/main.py
    from tools.my_complex_logic import perform_complex_task

    @mcp.tool()
    async def my_complex_tool(ctx: Context, data: str) -> str:
        """A tool that performs a complex, delegated task."""
        result = perform_complex_task(data) # Logic is in tools/my_complex_logic.py
        return f"Complex task result: {result}"
    ```

3.  **Manage dependencies**:
    If your tools require external libraries (e.g., for API calls, database interactions), add them to `pyproject.toml` under `dependencies` and run `uv pip install -e .`.

4.  **Implement lifespan functions**:
    If your MCP needs to initialize resources (like database connections, API clients) once at startup, use the `lifespan` argument in `FastMCP` as shown in `src/main.py`.

5.  **Add resources and prompts**:
    Use `@mcp.resource()` and `@mcp.prompt()` decorators for more advanced MCP functionalities.

## Project Structure

```
.
├── pyproject.toml          # Project metadata and dependencies
├── .env.example            # Example environment variables
├── .gitignore              # Files to ignore in version control
├── Dockerfile              # Docker build instructions
├── README.md               # Project documentation
├── LICENSE                 # Project license
├── src/                    # Source code for the MCP server
│   ├── main.py             # Main MCP server application (defines exposed tools)
│   └── utils.py            # Utility functions
├── docs/                   # Project-specific documentation
├── tests/                  # Unit and integration tests
└── tools/                  # Modular implementations of complex tool logic
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.