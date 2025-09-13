# Look 4 Fundings - MCP Server

A Model Context Protocol (MCP) server that provides tools for text manipulation and analysis. This server is designed to work with Le Chat and other MCP-compatible clients.

## Features

- **Text Inversion**: Reverse the characters in any word
- **Character Counting**: Count occurrences of specific characters in strings
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

The server will start on `http://localhost:8000` and use the streamable-http transport for Le Chat compatibility.

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
lt --port 8000
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

### `invert_word`
Reverses the characters in a given word.

**Parameters:**
- `word` (str): The word to invert

**Returns:**
- `str`: The inverted word

**Example:**
```
Input: "hello"
Output: "olleh"
```

### `count_r_occurences_in_string`
Counts the number of 'r' characters in a string.

**Parameters:**
- `string` (str): The input string to analyze

**Returns:**
- `int`: The number of 'r' characters found

**Example:**
```
Input: "programming"
Output: 2
```

## Development

This project uses:
- **FastMCP**: For building the MCP server
- **Streamable HTTP**: For Le Chat compatibility
- **Python 3.12+**: For modern Python features

## Troubleshooting

- **Port already in use**: If port 8000 is occupied, you can modify the port in `main.py` and update the LocalTunnel command accordingly
- **LocalTunnel issues**: Make sure LocalTunnel is installed globally and the tunnel URL is accessible
- **Le Chat connection**: Ensure the MCP endpoint URL includes `/mcp` at the end

## License

This project is open source and available under the MIT License.
