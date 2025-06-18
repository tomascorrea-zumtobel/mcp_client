"""
MCP Client - Core client implementation for Model Context Protocol.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from mcp import ClientSession, StdioServerParameters  
from mcp.client.stdio import stdio_client
from mcp.types import CallToolRequest, ListToolsRequest, Tool


@dataclass
class MCPServerConfig:
    """Configuration for an MCP server connection."""
    name: str
    command: str
    args: List[str]
    env: Optional[Dict[str, str]] = None


class MCPClient:
    """Core MCP Client for managing server connections and tool execution."""
    
    def __init__(self):
        self.sessions: Dict[str, ClientSession] = {}
        self.server_configs: Dict[str, MCPServerConfig] = {}
        self.logger = logging.getLogger(__name__)
        
    async def add_server(self, config: MCPServerConfig) -> bool:
        """Connect to an MCP server."""
        try:
            server_params = StdioServerParameters(
                command=config.command,
                args=config.args,
                env=config.env or {}
            )
            
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    self.sessions[config.name] = session
                    self.server_configs[config.name] = config
                    return True
                    
        except Exception as e:
            self.logger.error(f"Failed to connect to {config.name}: {e}")
            return False
    
    async def list_tools(self, server_name: Optional[str] = None) -> Dict[str, List[Tool]]:
        """List available tools from one or all servers."""
        tools_by_server = {}
        servers_to_check = [server_name] if server_name else list(self.sessions.keys())
        
        for name in servers_to_check:
            if name in self.sessions:
                try:
                    session = self.sessions[name]
                    request = ListToolsRequest()
                    response = await session.list_tools(request)
                    tools_by_server[name] = response.tools
                except Exception as e:
                    self.logger.error(f"Failed to list tools for {name}: {e}")
                    tools_by_server[name] = []
        
        return tools_by_server
    
    async def call_tool(self, server_name: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool on a specific server."""
        if server_name not in self.sessions:
            return {"error": f"Server {server_name} not connected"}
        
        try:
            session = self.sessions[server_name]
            request = CallToolRequest(name=tool_name, arguments=arguments)
            response = await session.call_tool(request)
            
            return {
                "success": True,
                "result": response.content
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_connected_servers(self) -> List[str]:
        """Get list of connected server names."""
        return list(self.sessions.keys())
    
    async def disconnect_all(self):
        """Disconnect from all servers."""
        self.sessions.clear()
        self.server_configs.clear()
