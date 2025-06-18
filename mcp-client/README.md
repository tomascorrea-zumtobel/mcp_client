"""
MCP Client Application - Clean Modular Architecture
==================================================

This MCP Client application provides a clean, modular structure for connecting to and interacting with MCP (Model Context Protocol) servers.

## Project Structure

```
mcp-client/
├── main.py                 # Main entry point
├── cli.py                  # Command-line interface (legacy)
├── client/                 # Core client modules
│   ├── __init__.py
│   ├── core.py             # Main MCP Client class
│   ├── health/             # Health monitoring
│   │   ├── __init__.py
│   │   └── monitor.py      # Health checks and ping
│   ├── demo/               # Examples and demos
│   │   ├── __init__.py
│   │   └── examples.py     # Demo scenarios
│   └── test/               # Testing utilities
│       ├── __init__.py
│       └── runner.py       # Test suite
├── pyproject.toml          # Dependencies
└── README.md               # This file
```

## Core Components

### 1. **client/core.py** - Main MCP Client class
   - Server connection management
   - Tool listing and execution
   - Clean, minimal implementation

### 2. **client/health/monitor.py** - Health monitoring
   - Server ping functionality
   - Health checks for all connected servers
   - Status reporting with timestamps

### 3. **client/demo/examples.py** - Demonstrations
   - Basic usage examples
   - Mock server configurations
   - Learning scenarios

### 4. **client/test/runner.py** - Test suite
   - Unit tests for core functionality
   - Validation of error handling
   - Automated testing

## Features Implemented

✅ Modular, clean code architecture
✅ Basic MCP Client structure
✅ Health monitoring and ping endpoints
✅ Server connection management
✅ Tool listing and execution
✅ Error handling
✅ Comprehensive test suite
✅ Demo functionality

## Usage

### Quick Commands

```bash
# Check status
uv run python main.py status

# Run all tests
uv run python main.py test

# Run demo
uv run python main.py demo
```

### Legacy CLI (still available)
```bash
uv run python cli.py status
uv run python cli.py health
```

## Next Steps

To connect to actual MCP servers, use the MCPServerConfig class:

```python
from client.core import MCPClient, MCPServerConfig
from client.health.monitor import HealthMonitor

# Create client
client = MCPClient()
health_monitor = HealthMonitor(client)

# Configure server
config = MCPServerConfig(
    name="my-server",
    command="path/to/server",
    args=["--arg1", "value1"],
    env={"ENV_VAR": "value"}
)

# Connect
await client.add_server(config)

# Check health
health = await health_monitor.health_check()
```

## Architecture Benefits

- **Separation of Concerns**: Each module has a single responsibility
- **Easy Testing**: Isolated components for unit testing
- **Extensible**: Easy to add new tools and functionality
- **Clean Imports**: Proper package structure
- **Maintainable**: Clear organization for future development

The foundation is solid and ready for real MCP server integrations!
