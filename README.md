# MCP Client - German Learning Project

A Model Context Protocol (MCP) client project for German language learning with translation capabilities and database storage. This project demonstrates integration with multiple MCP servers including DeepL translation, PostgreSQL database, and web fetching capabilities.

## Features

- 🌍 **Translation**: German ↔ English ↔ Spanish translation using DeepL API
- 🗃️ **Database Storage**: PostgreSQL database for storing translations with timestamps
- 🔍 **Web Fetching**: Fetch content from web URLs for language learning materials
- 🤖 **GitHub Copilot Integration**: Works seamlessly with GitHub Copilot's Agent mode

## Prerequisites

- [Docker](https://www.docker.com/get-started) and Docker Compose
- [uv](https://docs.astral.sh/uv/) - Python package manager
- [Node.js](https://nodejs.org/) - For DeepL MCP server
- [GitHub Copilot](https://github.com/features/copilot) subscription
- [DeepL API key](https://www.deepl.com/pro-api) (free tier available)

## Setup Instructions

### 1. Clone and Navigate to Project

```bash
git clone <repository-url>
cd mcp_client
```

### 2. Environment Configuration

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit the `.env` file with your credentials, based in the .env.example

### 3. Database Setup

Start the PostgreSQL database using Docker Compose:

```bash
docker-compose up -d
```

The database will automatically:
- Create the `german_learning` database
- Run the initialization script (`database/init.sql`)
- Create the `translations` table
- Insert sample translation data
- Be available on port `5434`

Verify the database is running:

```bash
docker-compose ps
```

### 4. MCP Configuration

Run the setup script to configure MCP with your API keys:

```bash
chmod +x setup-mcp.sh
./setup-mcp.sh
```

This will create the `.vscode/mcp.json` file with your DeepL API key and database configuration.

### 5. Install Python Dependencies

```bash
cd mcp-client
uv sync
```

## Usage

### GitHub Copilot Agent Mode

1. **Enable MCP in VS Code**: Ensure the `.vscode/mcp.json` file is properly configured
2. **Open GitHub Copilot Chat**: Use `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac) and select "GitHub Copilot: Open Chat"
3. **Use Agent Mode**: Start your queries with `@` to access MCP capabilities

#### Example Usage in Copilot Chat

```
# Translate and store in database
Translate "Ich bin müde" to Spanish and add it to the database

# Query database
Show me all translations from the database

# Fetch and translate web content
Fetch content from https://example-german-site.com and translate key phrases

# Database analysis
Show me the most recently added translations
```

## Database Schema

The `translations` table stores language learning data:

```sql
CREATE TABLE translations (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    german TEXT NOT NULL,
    english TEXT,
    spanish TEXT
);
```

## MCP Servers Configuration

This project uses three MCP servers:

1. **DeepL Translation Server**
   - Command: `npx -y deepl-mcp-server`
   - Purpose: High-quality translations between German, English, and Spanish

2. **PostgreSQL Database Server**
   - Command: `uv run postgres-mcp --access-mode=unrestricted`
   - Purpose: Store and query translation data

3. **Fetch Server**
   - Command: `uvx mcp-server-fetch`
   - Purpose: Retrieve content from web URLs for translation practice

## Troubleshooting

### Database Connection Issues

```bash
# Check if database is running
docker-compose ps

# View database logs
docker-compose logs postgres

# Restart database
docker-compose restart postgres
```

### MCP Configuration Issues

```bash
# Recreate MCP configuration
rm .vscode/mcp.json
./setup-mcp.sh
```

### DeepL API Issues

- Verify your API key in the `.env` file
- Check your DeepL API usage limits
- Ensure you're using the correct API endpoint (free vs. pro)

## Project Structure

```
mcp_client/
├── .env.example              # Environment variables template
├── .env                      # Your environment variables (not in git)
├── README.md                 # This file
├── docker-compose.yml        # Database container configuration
├── setup-mcp.sh             # MCP setup script
├── database/
│   └── init.sql             # Database initialization script
├── mcp-client/
│   ├── client.py            # MCP client implementation
│   ├── pyproject.toml       # Python dependencies
│   └── uv.lock             # Dependency lock file
└── .vscode/
    └── mcp.json             # MCP server configuration (auto-generated)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with both direct client and GitHub Copilot
5. Submit a pull request

