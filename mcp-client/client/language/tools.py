"""Language learning tools using Dictionary API and Datamuse API."""

import asyncio
import aiohttp
from typing import Dict, List, Any


class LanguageTools:
    """Language learning tools for definitions, synonyms, and antonyms."""
    
    def __init__(self):
        self.dict_api_base = "https://api.dictionaryapi.dev/api/v2/entries"
        self.datamuse_base = "https://api.datamuse.com/words"
    
    async def get_definition(self, word: str, language: str = "en") -> Dict[str, Any]:
        """Get word definition with part of speech and examples."""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.dict_api_base}/{language}/{word.lower()}"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._format_definition(data)
                    else:
                        return {"error": f"Definition not found for '{word}'"}
        except Exception as e:
            return {"error": f"API error: {str(e)}"}
    
    async def get_synonyms(self, word: str, language: str = "en") -> Dict[str, Any]:
        """Get synonyms using Datamuse API."""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.datamuse_base}?rel_syn={word.lower()}&max=10"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        synonyms = [item['word'] for item in data]
                        return {"word": word, "synonyms": synonyms}
                    else:
                        return {"error": f"Synonyms not found for '{word}'"}
        except Exception as e:
            return {"error": f"API error: {str(e)}"}
    
    async def get_antonyms(self, word: str, language: str = "en") -> Dict[str, Any]:
        """Get antonyms using Datamuse API."""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.datamuse_base}?rel_ant={word.lower()}&max=10"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        antonyms = [item['word'] for item in data]
                        return {"word": word, "antonyms": antonyms}
                    else:
                        return {"error": f"Antonyms not found for '{word}'"}
        except Exception as e:
            return {"error": f"API error: {str(e)}"}
    
    def _format_definition(self, data: List[Dict]) -> Dict[str, Any]:
        """Format dictionary API response."""
        if not data:
            return {"error": "No definition found"}
        
        entry = data[0]
        result = {
            "word": entry.get("word", ""),
            "phonetics": [p.get("text", "") for p in entry.get("phonetics", []) if p.get("text")],
            "definitions": []
        }
        
        for meaning in entry.get("meanings", []):
            part_of_speech = meaning.get("partOfSpeech", "")
            for definition in meaning.get("definitions", []):
                result["definitions"].append({
                    "partOfSpeech": part_of_speech,
                    "definition": definition.get("definition", ""),
                    "example": definition.get("example", "")
                })
        
        return result
