"""
Health monitoring and ping functionality for MCP Client.
"""

import asyncio
from datetime import datetime
from typing import Dict, Any
from mcp.types import ListToolsRequest


class HealthMonitor:
    """Handles health checks and ping operations for MCP servers."""
    
    def __init__(self, client):
        self.client = client
    
    async def ping_server(self, server_name: str) -> Dict[str, Any]:
        """Ping a specific MCP server to check its health."""
        timestamp = datetime.now().isoformat()
        
        if server_name not in self.client.sessions:
            return {
                "server": server_name,
                "status": "not_connected",
                "timestamp": timestamp,
                "error": "Server not found or not connected"
            }
        
        try:
            session = self.client.sessions[server_name]
            tools_request = ListToolsRequest()
            tools_response = await session.list_tools(tools_request)
            
            return {
                "server": server_name,
                "status": "healthy",
                "timestamp": timestamp,
                "tools_count": len(tools_response.tools)
            }
            
        except Exception as e:
            return {
                "server": server_name,
                "status": "unhealthy",
                "timestamp": timestamp,
                "error": str(e)
            }
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on all connected servers."""
        health_status = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "healthy",
            "servers": {},
            "summary": {
                "total_servers": len(self.client.sessions),
                "healthy_servers": 0,
                "unhealthy_servers": 0
            }
        }
        
        for server_name in self.client.sessions.keys():
            ping_result = await self.ping_server(server_name)
            health_status["servers"][server_name] = ping_result
            
            if ping_result["status"] == "healthy":
                health_status["summary"]["healthy_servers"] += 1
            else:
                health_status["summary"]["unhealthy_servers"] += 1
        
        if health_status["summary"]["unhealthy_servers"] > 0:
            health_status["overall_status"] = "degraded"
        
        if health_status["summary"]["healthy_servers"] == 0 and health_status["summary"]["total_servers"] > 0:
            health_status["overall_status"] = "unhealthy"
        
        return health_status
