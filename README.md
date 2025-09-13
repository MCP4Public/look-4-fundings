# Look 4 Fundings - EU Funding Crawler MCP Server

A Model Context Protocol (MCP) server that provides tools for searching EU funding opportunities through the official EU Funding & Tenders Portal API. This server is designed to work with Le Chat and other MCP-compatible clients.

## Features

- **EU Funding Search**: Search for active EU funding opportunities by keyword
- **Comprehensive Data**: Get detailed information including title, summary, deadline, budget, and status
- **Official API Integration**: Uses the official EU Funding & Tenders Portal REST API
- **Le Chat Integration**: Compatible with Le Chat's MCP connector system

## Prerequisites

- Python 3.12 or higher
- `uv` package manager

## Installation

1. Clone or download this repository
2. Install dependencies using `uv`:

```bash
uv sync
```

## Running the Server

### Method 1: Direct Python Execution

Run the server directly with Python:

```bash
python main.py
```

The server will start on `http://localhost:3000` and use the streamable-http transport for Le Chat compatibility.

### Method 2: Using LocalTunnel for External Access

To expose your local server to the internet (required for Le Chat integration), use `lt` (LocalTunnel):

1. Install LocalTunnel globally:
```bash
npm install -g localtunnel
```

2. In one terminal, start the MCP server:
```bash
python main.py
```

3. In another terminal, expose the server using LocalTunnel:
```bash
lt --port 3000
```

This will provide you with a public URL like `https://legal-bugs-chew.loca.lt` that you can use to connect to your MCP server.

## Le Chat Integration

To connect this MCP server to Le Chat:

1. Start your MCP server using one of the methods above
2. If using LocalTunnel, note the provided URL (e.g., `https://legal-bugs-chew.loca.lt`)
3. In Le Chat, go to the connectors section
4. Add a new MCP connector with the URL: `https://your-tunnel-url.loca.lt/mcp`
5. The server will be available for use in Le Chat

## Available Tools

### `search_eu_fundings`
Searches for EU funding opportunities by keyword and returns detailed funding information.

**Parameters:**
- `keyword` (str): The search keyword (e.g., "AI", "machine learning", "renewable energy") - defaults to "AI"
- `page_size` (int): Number of results to return per page - defaults to 20

**Returns:**
- `List[PublicFunding]`: A list of PublicFunding objects containing:
  - `title` (str): Title of the funding opportunity
  - `url` (str): Direct link to the funding page
  - `summary` (str): Summary/objective of the funding
  - `deadline` (str): Application deadline
  - `status` (str): Current status of the funding
  - `budget` (str): Budget information with currency

**Example:**
```
Input: keyword="artificial intelligence", page_size=10
Output: List of 10 EU funding opportunities related to AI
```

**Note:** Returns an empty list if no results are found or if an error occurs during the API request.

## Development

This project uses:
- **FastMCP**: For building the MCP server
- **Streamable HTTP**: For Le Chat compatibility
- **Python 3.12+**: For modern Python features
- **Pydantic**: For data validation and serialization
- **Requests**: For HTTP API calls to the EU Funding Portal
- **EU Funding & Tenders Portal API**: Official REST API for funding data

## Project Structure

- `main.py`: MCP server setup and tool definitions
- `crawler.py`: EUFundingCrawler class for API interactions
- `type.py`: Pydantic models for data structures
- `pyproject.toml`: Project dependencies and configuration

## Troubleshooting

- **Port already in use**: If port 3000 is occupied, you can modify the port in `main.py` and update the LocalTunnel command accordingly
- **LocalTunnel issues**: Make sure LocalTunnel is installed globally and the tunnel URL is accessible
- **Le Chat connection**: Ensure the MCP endpoint URL includes `/mcp` at the end
- **API errors**: The crawler uses the official EU API which may have rate limits or temporary unavailability
- **No results found**: Try different keywords or check if the API is responding correctly

## License

This project is open source and available under the MIT License.
