# Simple DeepL MCP Client

A simple Python client for using DeepL translation through MCP with VS Code and GitHub Copilot.

## Quick Setup

1. **Get DeepL API Key**: Sign up at https://www.deepl.com/pro-api
2. **Add your key to .env**:
   ```bash
   DEEPL_AUTH_KEY=your_actual_key_here
   ```
3. **Test it**:
   ```bash
   uv run python simple_deepl.py
   ```

## Usage with VS Code

Use the functions in `simple_deepl.py` with GitHub Copilot:

```python
# Translate text
result = await translate_text("Hello world", "ES")

# Get supported languages  
languages = await get_languages()
```

## Available Languages

Common language codes:
- `ES` - Spanish
- `FR` - French  
- `DE` - German
- `IT` - Italian
- `PT` - Portuguese
- `RU` - Russian
- `JA` - Japanese
- `ZH` - Chinese

That's it! Simple and focused on what you need.