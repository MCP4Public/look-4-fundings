from mcp.server.fastmcp import FastMCP
from crawler import EUFundingCrawler
from typing import List, Optional
from type import PublicFunding, MyCompany
import httpx

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


@mcp.tool()
def get_company_profile() -> Optional[MyCompany]:
    """
    Retrieve the company profile information from the Look 4 Fundings web application.

    This tool fetches the current company profile data from the deployed web application
    to provide context about the company's information for better funding recommendations.

    Returns:
        Optional[MyCompany]: The company profile object containing name, URL, and scope.
            Returns None if no company profile is set or if there's an error.
    """
    try:
        with httpx.Client() as client:
            response = client.get(
                "https://web-production-08f4.up.railway.app/api/company"
            )
            response.raise_for_status()

            if response.status_code == 200:
                data = response.json()
                if data is None:
                    return None
                return MyCompany(**data)
            return None
    except Exception as e:
        print(f"Error fetching company profile: {e}")
        return None


@mcp.tool()
def add_grant_with_affinity(
    funding: PublicFunding, affinity_score: float
) -> Optional[PublicFunding]:
    """
    Add a new grant to the Look 4 Fundings web application with a specified affinity score.

    This tool takes a PublicFunding object, updates its company_affinity field with the provided
    affinity score, and creates a new grant entry in the web application.

    Args:
        funding (PublicFunding): The funding opportunity object to add
        affinity_score (float): The company affinity score (0-100) for this funding opportunity

    Returns:
        Optional[PublicFunding]: The created funding object with updated affinity score.
            Returns None if there's an error during creation.
    """
    try:
        # Validate affinity score
        if not 0 <= affinity_score <= 100:
            raise ValueError("Affinity score must be between 0 and 100")

        # Create a copy of the funding object with updated affinity
        updated_funding = PublicFunding(
            title=funding.title,
            url=funding.url,
            summary=funding.summary,
            deadline=funding.deadline,
            status=funding.status,
            budget=funding.budget,
            company_affinity=affinity_score,
        )

        # Convert to dict for JSON serialization with proper date handling
        funding_data = updated_funding.dict()
        # Manually convert date to string for JSON serialization
        if "deadline" in funding_data:
            funding_data["deadline"] = funding_data["deadline"].isoformat()
        print(f"DEBUG: Sending funding data: {funding_data}")

        with httpx.Client() as client:
            response = client.post(
                "https://web-production-08f4.up.railway.app/api/grants",
                json=funding_data,
                headers={"Content-Type": "application/json"},
            )
            print(f"DEBUG: Response status: {response.status_code}")
            print(f"DEBUG: Response content: {response.text}")
            response.raise_for_status()

            if response.status_code == 200:
                return updated_funding
            return None

    except Exception as e:
        print(f"Error adding grant with affinity: {e}")
        return None


def main():
    # Use streamable-http for Le Chat compatibility
    # Use lt --port 8000 to expose the server
    # copy paster the url to the Le Chat with https://legal-bugs-chew.loca.lt/mcp/
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
