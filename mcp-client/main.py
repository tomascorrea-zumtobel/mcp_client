#!/usr/bin/env python3
"""
Main entry point for MCP Client.
Provides simple command-line interface for testing and interaction.
"""

import asyncio
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from client.core import MCPClient, MCPServerConfig
from client.health.monitor import HealthMonitor


async def quick_status():
    """Quick status check."""
    client = MCPClient()
    health_monitor = HealthMonitor(client)
    
    print("🔧 MCP Client Status:")
    print(f"Connected servers: {len(client.get_connected_servers())}")
    
    health = await health_monitor.health_check()
    print(f"Overall status: {health['overall_status']}")
    
    return client, health_monitor


async def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "status":
            await quick_status()
        elif command == "test":
            # Run tests
            from client.test.runner import run_tests
            await run_tests()
        elif command == "demo":
            # Run demo
            from client.demo.examples import basic_demo
            await basic_demo()
        else:
            print(f"Unknown command: {command}")
            print("Available commands: status, test, demo")
    else:
        print("🚀 MCP Client")
        await quick_status()


if __name__ == "__main__":
    asyncio.run(main())
