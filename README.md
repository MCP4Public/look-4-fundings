# Look 4 Fundings - EU Funding Crawler MCP Server

A Model Context Protocol (MCP) server that provides tools for searching EU funding opportunities and managing company funding data through the Look 4 Fundings web application. This server integrates with both the official EU Funding & Tenders Portal API and the Look 4 Fundings web platform.

## Features

- **EU Funding Search**: Search for active EU funding opportunities by keyword
- **Company Profile Management**: Retrieve company information for better funding recommendations
- **Grant Management**: Add funding opportunities to the web application with custom affinity scores
- **Professional Reports**: Generate PDF reports from company data and won grants
- **Report Generation**: Create both generated reports (from website data) and API reports (from custom content)
- **Comprehensive Data**: Get detailed information including title, summary, deadline, budget, and status
- **Dual API Integration**: Uses both the official EU Funding & Tenders Portal API and the Look 4 Fundings web API
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
  - `deadline` (date): Application deadline
  - `status` (str): Current status of the funding
  - `budget` (str): Budget information with currency
  - `company_affinity` (float): Company affinity score (0-100)
  - `won` (bool): Whether the grant was won or not (default: False)

**Example:**
```
Input: keyword="artificial intelligence", page_size=10
Output: List of 10 EU funding opportunities related to AI
```

**Note:** Returns an empty list if no results are found or if an error occurs during the API request.

### `get_company_profile`
Retrieves the company profile information from the Look 4 Fundings web application.

**Parameters:**
- None

**Returns:**
- `Optional[MyCompany]`: The company profile object containing:
  - `name` (str): Name of the company
  - `url` (str): Direct link to the company's website
  - `scope` (str): Description of the company's scope/activities

**Example:**
```
Input: None
Output: MyCompany(name="EcoTech Solutions", url="https://ecotechsolutions.com", scope="AI-powered environmental solutions")
```

**Note:** Returns `None` if no company profile is set or if there's an error fetching the data.

### `add_grant_with_affinity`
Adds a new grant to the Look 4 Fundings web application with a specified affinity score.

**Parameters:**
- `funding` (PublicFunding): The funding opportunity object to add
- `affinity_score` (float): The company affinity score (0-100) for this funding opportunity

**Returns:**
- `Optional[PublicFunding]`: The created funding object with updated affinity score, or `None` if there's an error

**Example:**
```
Input: funding=PublicFunding(...), affinity_score=85.5
Output: PublicFunding object with company_affinity=85.5
```

**Note:** The function validates that the affinity score is between 0 and 100. The funding object is automatically updated with the new affinity score before being posted to the web application. The `won` field is preserved from the original funding object.

### `get_grants`
Retrieves all grants currently listed in the Look 4 Fundings web application.

**Parameters:**
- None

**Returns:**
- `List[PublicFunding]`: A list of all PublicFunding objects currently in the application, including their won status

**Example:**
```
Input: None
Output: List of all grants with their current won status
```

**Note:** Returns an empty list if no grants are found or if there's an error. The function automatically converts date strings back to date objects for proper data handling.

### `generate_company_report`
Generates a professional PDF report for the company using profile and grants data.

**Parameters:**
- `report_content` (str): Optional custom report content. If empty, generates report from website data (company profile + won grants)

**Returns:**
- `Optional[dict]`: Report generation result with download URL and details, or `None` if error

**Report Types:**
- **Generated Reports**: Automatically created from company profile and won grants data
- **API Reports**: Created from custom LLM-generated content

**Example:**
```
Input: report_content=""
Output: {"success": True, "report_name": "Generated Report", "download_url": "https://...", "message": "Report generated successfully"}

Input: report_content="Our company has shown strong performance in clean technology grants..."
Output: {"success": True, "report_name": "API Report", "download_url": "https://...", "message": "Report generated successfully"}
```

**Note:** The tool automatically determines the report type based on whether content is provided. Generated reports include company information, grant statistics, and won grants details. API reports use the provided custom content.

## Development

This project uses:
- **FastMCP**: For building the MCP server
- **Streamable HTTP**: For Le Chat compatibility
- **Python 3.12+**: For modern Python features
- **Pydantic**: For data validation and serialization
- **Requests**: For HTTP API calls to the EU Funding Portal
- **HTTPX**: For HTTP API calls to the Look 4 Fundings web application
- **ReportLab**: For PDF report generation
- **EU Funding & Tenders Portal API**: Official REST API for funding data
- **Look 4 Fundings Web API**: Custom web application API for grant management and reports

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
- **Date serialization errors**: The `add_grant_with_affinity` tool automatically handles date conversion for JSON serialization
- **Web API connection**: Ensure the Look 4 Fundings web application is accessible at `https://web-production-08f4.up.railway.app/`
- **Affinity score validation**: The affinity score must be between 0 and 100, inclusive
- **Report generation errors**: Ensure the web application has ReportLab installed and the reports API is accessible
- **PDF download issues**: Reports are generated server-side and downloaded via the web application's download endpoint

## License

This project is open source and available under the MIT License.
