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
        elif command == "define":
            # Get word definition
            word = sys.argv[2] if len(sys.argv) > 2 else input("Enter word: ")
            lang = sys.argv[3] if len(sys.argv) > 3 else "en"
            from client.language.tools import LanguageTools
            tools = LanguageTools()
            result = await tools.get_definition(word, lang)
            print(f"📖 Definition for '{word}':")
            if "error" in result:
                print(f"❌ {result['error']}")
            else:
                if result.get("phonetics"):
                    print(f"🔊 Pronunciation: {', '.join(result['phonetics'])}")
                for def_item in result.get("definitions", []):
                    print(f"• {def_item['partOfSpeech']}: {def_item['definition']}")
                    if def_item.get('example'):
                        print(f"  Example: {def_item['example']}")
        elif command == "synonyms":
            # Get synonyms
            word = sys.argv[2] if len(sys.argv) > 2 else input("Enter word: ")
            from client.language.tools import LanguageTools
            tools = LanguageTools()
            result = await tools.get_synonyms(word)
            print(f"🔄 Synonyms for '{word}':")
            if "error" in result:
                print(f"❌ {result['error']}")
            else:
                print(f"• {', '.join(result['synonyms'])}")
        elif command == "antonyms":
            # Get antonyms
            word = sys.argv[2] if len(sys.argv) > 2 else input("Enter word: ")
            from client.language.tools import LanguageTools
            tools = LanguageTools()
            result = await tools.get_antonyms(word)
            print(f"↔️ Antonyms for '{word}':")
            if "error" in result:
                print(f"❌ {result['error']}")
            else:
                print(f"• {', '.join(result['antonyms'])}")
        else:
            print(f"Unknown command: {command}")
            print("Available commands: status, test, demo, define, synonyms, antonyms")
    else:
        print("🚀 MCP Client")
        await quick_status()


if __name__ == "__main__":
    asyncio.run(main())
