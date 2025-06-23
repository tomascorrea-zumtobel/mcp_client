#!/usr/bin/env python3
"""
MCP Server for Language Tools
Exposes define, synonyms, and antonyms as MCP tools
"""

import asyncio
import json
import sys
from typing import Any, Sequence

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)
import mcp.server.stdio
import mcp.types as types

from client.language.tools import LanguageTools

# Create server instance
server = Server("language-tools")

# Initialize language tools
language_tools = LanguageTools()

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="define",
            description="Get definition of a word with part of speech and examples",
            inputSchema={
                "type": "object",
                "properties": {
                    "word": {
                        "type": "string",
                        "description": "The word to define"
                    },
                    "language": {
                        "type": "string",
                        "description": "Language code (default: en)",
                        "default": "en"
                    }
                },
                "required": ["word"]
            }
        ),
        Tool(
            name="synonyms",
            description="Get synonyms for a word",
            inputSchema={
                "type": "object",
                "properties": {
                    "word": {
                        "type": "string",
                        "description": "The word to find synonyms for"
                    }
                },
                "required": ["word"]
            }
        ),
        Tool(
            name="antonyms",
            description="Get antonyms for a word",
            inputSchema={
                "type": "object",
                "properties": {
                    "word": {
                        "type": "string",
                        "description": "The word to find antonyms for"
                    }
                },
                "required": ["word"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
    """Handle tool calls."""
    try:
        if name == "define":
            word = arguments.get("word", "")
            language = arguments.get("language", "en")
            
            if not word:
                return [types.TextContent(
                    type="text",
                    text="Error: Word parameter is required"
                )]
            
            result = await language_tools.get_definition(word, language)
            
            if "error" in result:
                return [types.TextContent(
                    type="text",
                    text=f"❌ {result['error']}"
                )]
            
            # Format the definition response
            response = f"📖 Definition for '{word}':\n"
            if result.get("phonetics"):
                response += f"🔊 Pronunciation: {', '.join(result['phonetics'])}\n"
            
            for def_item in result.get("definitions", []):
                response += f"• {def_item['partOfSpeech']}: {def_item['definition']}\n"
                if def_item.get('example'):
                    response += f"  Example: {def_item['example']}\n"
            
            return [types.TextContent(type="text", text=response)]
            
        elif name == "synonyms":
            word = arguments.get("word", "")
            
            if not word:
                return [types.TextContent(
                    type="text",
                    text="Error: Word parameter is required"
                )]
            
            result = await language_tools.get_synonyms(word)
            
            if "error" in result:
                return [types.TextContent(
                    type="text",
                    text=f"❌ {result['error']}"
                )]
            
            response = f"🔄 Synonyms for '{word}':\n"
            if result.get("synonyms"):
                response += f"• {', '.join(result['synonyms'])}"
            else:
                response += "• No synonyms found"
            
            return [types.TextContent(type="text", text=response)]
            
        elif name == "antonyms":
            word = arguments.get("word", "")
            
            if not word:
                return [types.TextContent(
                    type="text",
                    text="Error: Word parameter is required"
                )]
            
            result = await language_tools.get_antonyms(word)
            
            if "error" in result:
                return [types.TextContent(
                    type="text",
                    text=f"❌ {result['error']}"
                )]
            
            response = f"↔️ Antonyms for '{word}':\n"
            if result.get("antonyms"):
                response += f"• {', '.join(result['antonyms'])}"
            else:
                response += "• No antonyms found"
            
            return [types.TextContent(type="text", text=response)]
            
        else:
            return [types.TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]
            
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]

async def main():
    """Run the server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
