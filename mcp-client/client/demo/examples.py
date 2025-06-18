"""
Demo and testing functionality for MCP Client.
"""

import asyncio
import json
import logging
import sys
import os

# Add parent directories to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client.core import MCPClient, MCPServerConfig
from client.health.monitor import HealthMonitor


def setup_logging():
    """Set up basic logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


async def basic_demo():
    """Basic demo showing MCP client functionality."""
    setup_logging()
    
    client = MCPClient()
    health_monitor = HealthMonitor(client)
    
    print("=== MCP Client Basic Demo ===")
    print(f"Connected servers: {client.get_connected_servers()}")
    
    # Health check with no servers
    print("\n=== Initial Health Check ===")
    health = await health_monitor.health_check()
    print(json.dumps(health, indent=2))
    
    return client, health_monitor


async def test_with_mock_server():
    """Test with a mock or example server configuration."""
    client, health_monitor = await basic_demo()
    
    # Example configuration (won't actually connect without real server)
    example_config = MCPServerConfig(
        name="example-server",
        command="echo",
        args=["hello"],
        env={}
    )
    
    print(f"\n=== Example Server Config ===")
    print(f"Name: {example_config.name}")
    print(f"Command: {example_config.command}")
    print(f"Args: {example_config.args}")
    
    # Try to list tools (will be empty since no servers connected)
    tools = await client.list_tools()
    print(f"\n=== Available Tools ===")
    print(json.dumps(tools, indent=2))
    
    return client, health_monitor


if __name__ == "__main__":
    asyncio.run(test_with_mock_server())
