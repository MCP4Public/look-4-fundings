import requests
from typing import Dict, Any, List
from type import PublicFunding


class EUFundingCrawler:
    """
    A crawler for the EU Funding & Tenders Portal using the official REST API.
    Uses only requests, httpx, and urllib as requested.
    """

    # Official API endpoints
    SEARCH_API_URL = "https://api.tech.ec.europa.eu/search-api/prod/rest/search"
    FACET_API_URL = "https://api.tech.ec.europa.eu/search-api/prod/rest/facet"
    API_KEY = "SEDIA_NONH2020_PROD"

    def __init__(self):
        """Initialize the crawler."""
        self.session = requests.Session()
        self._setup_session()

    def _setup_session(self):
        """Setup the requests session with appropriate headers."""
        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/125.0.0.0 Safari/537.36"
                ),
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
            }
        )

    def _build_search_query(self, keyword: str, **kwargs) -> Dict[str, Any]:
        """
        Build the search query for the API.

        Args:
            keyword (str): The search keyword
            **kwargs: Additional search parameters

        Returns:
            Dict[str, Any]: The query data for the API
        """
        # Base query structure for grants and tenders
        query = {
            "bool": {
                "must": [
                    {
                        "terms": {
                            "type": ["0"]  # All grants and tenders
                        }
                    },
                    {
                        "terms": {
                            "status": ["31094501", "31094502"]  # Active statuses
                        }
                    },
                ]
            }
        }

        return query

    def _parse_results_to_public_funding(
        self, results: List[Dict[str, Any]]
    ) -> List[PublicFunding]:
        # from datetime import datetime
        # today = datetime.now().date()
        funding_list = []

        for idx, result in enumerate(results):
            # Parse dates - handle both string and list formats
            # start_date_str = result["metadata"]["startDate"]
            # Get end date with fallback to empty string
            try:
                end_date_str = result["metadata"].get("endDate", [""])[0] if result["metadata"].get("endDate") else ""
            except (KeyError, IndexError):
                end_date_str = ""

            # Get budget with fallback to empty string
            try:
                budget = result["metadata"].get("overallBudget", [""])[0]
                budget = budget + " €" if budget else ""
            except (KeyError, IndexError):
                budget = ""

            # Get summary/objective with fallback to empty string
            try:
                summary = result["metadata"].get("objective", [""])[0] if result["metadata"].get("objective") else ""
            except (KeyError, IndexError):
                summary = ""

            funding = PublicFunding(
                title=result.get("summary", ""),
                url=result.get("url", ""),
                summary=summary,
                deadline=end_date_str,
                status="TEST",
                budget=budget,
            )
            funding_list.append(funding)

        return funding_list

    def get_grants_and_tenders(
        self, keyword: str, page_size: int = 20
    ) -> List[PublicFunding]:
        """
        Try to get the count using the official API with requests.

        Args:
            keyword (str): The search keyword
            page_size (int): Number of results per page (default: 20)

        Returns:
            Optional[int]: The total count if found, None otherwise
        """
        try:
            # Build the API URL with parameters
            params = {
                "apiKey": self.API_KEY,
                "text": keyword if keyword else "*",
                "pageSize": page_size,
            }

            # Build the query data
            query_data = self._build_search_query(keyword)

            print(f"DEBUG - Parameters: {params}")

            # Make POST request to the API
            response = self.session.post(
                self.SEARCH_API_URL, params=params, json=query_data, timeout=30
            )

            print(f"DEBUG - Response Status: {response.status_code}")

            response.raise_for_status()

            # Parse the JSON response
            data = response.json()
            print(f"DEBUG - Response Data Keys: {list(data.keys())}")
            print(f"DEBUG - Response Data: {data['totalResults']}")
            print(
                f"DEBUG - Response Data First example: {data['results'][0]['metadata'].keys()}"
            )

            return self._parse_results_to_public_funding(data["results"])

        except Exception as e:
            print(f"API request failed: {e}")
            return []


def main():
    """Main function to demonstrate the crawler usage."""
    # Example usage
    crawler = EUFundingCrawler()

    # Search for AI-related funding opportunities
    result = crawler.get_grants_and_tenders(keyword="AI", page_size=20)

    if not result:
        print("No results found")

    print(result[0])


if __name__ == "__main__":
    main()
