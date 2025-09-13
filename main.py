from mcp.server.fastmcp import FastMCP
from crawler import EUFundingCrawler
from typing import List
from type import PublicFunding

# Create an MCP server
mcp = FastMCP(
    name="EU-Funding-Crawler",
    host="0.0.0.0",  # only used for SSE transport
    port=3000,  # only used for SSE transport (HF expect 7860 as a port)
    stateless_http=True,
    debug=True,
)

# Initialize the crawler
crawler = EUFundingCrawler()


@mcp.tool()
def search_eu_fundings(keyword="AI", page_size=20) -> List[PublicFunding]:
    """
    Search for EU funding opportunities by keyword and return a list of funding details.

    Args:
        keyword (str): The search keyword (e.g., "AI", "machine learning", "renewable energy")
        page_size (int): Number of results to return per page (default: 20)

    Returns:
        List[PublicFunding]: A list of PublicFunding objects containing funding details like
            title, URL, summary, deadline, status and budget. Returns empty list if no results
            or on error.
    """
    try:
        results = crawler.get_grants_and_tenders(keyword="AI", page_size=20)
        return results
    except Exception as e:
        print(f"Error: {e}")
        return []


def main():
    # Use streamable-http for Le Chat compatibility
    # Use lt --port 8000 to expose the server
    # copy paster the url to the Le Chat with https://legal-bugs-chew.loca.lt/mcp/
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
