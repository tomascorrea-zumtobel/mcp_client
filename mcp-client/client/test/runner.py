"""
Simple test runner for MCP Client functionality.
"""

import asyncio
import json
import sys
import os

# Add parent directories to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client.core import MCPClient
from client.health.monitor import HealthMonitor


async def test_client_basics():
    """Test basic client functionality."""
    print("🔧 Testing MCP Client Basics...")
    
    client = MCPClient()
    health_monitor = HealthMonitor(client)
    
    # Test 1: Initial state
    assert client.get_connected_servers() == []
    print("✅ Initial state: No servers connected")
    
    # Test 2: Health check with no servers
    health = await health_monitor.health_check()
    assert health["overall_status"] == "healthy"
    assert health["summary"]["total_servers"] == 0
    print("✅ Health check: Empty state is healthy")
    
    # Test 3: Ping non-existent server
    ping_result = await health_monitor.ping_server("non-existent")
    assert ping_result["status"] == "not_connected"
    print("✅ Ping test: Non-existent server properly handled")
    
    # Test 4: List tools with no servers
    tools = await client.list_tools()
    assert tools == {}
    print("✅ Tools listing: Empty when no servers")
    
    # Test 5: Call tool on non-existent server
    result = await client.call_tool("non-existent", "test-tool", {})
    assert "error" in result
    print("✅ Tool calling: Proper error handling")
    
    print("🎉 All basic tests passed!")
    return True


async def run_tests():
    """Run all tests."""
    try:
        await test_client_basics()
        print("\n🏆 All tests completed successfully!")
        return True
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(run_tests())
