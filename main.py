from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP(
    name="MCPTEST",
    host="0.0.0.0",  # only used for SSE transport
    port=3000,  # only used for SSE transport (HF expect 7860 as a port)
    stateless_http=True,
    debug=True
)


@mcp.tool()
def invert_word(word: str) -> str:
    """
    Invert a word by reversing its characters.

    Args:
        word (str): The word to invert

    Returns:
        str: The inverted word
    """
    inverted = word[::-1]
    return "".join(inverted)


@mcp.tool()
def count_r_occurences_in_string(string: str) -> int:
    """
    Count the number of 'r' occurrences in a string.

    Args:
        string (str): The input string to count 'r' characters in

    Returns:
        int: The number of 'r' characters found in the string
    """
    return string.count("r")


def main():
    # Use streamable-http for Le Chat compatibility
    # Use lt --port 8000 to expose the server
    # copy paster the url to the Le Chat with https://legal-bugs-chew.loca.lt/mcp/
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
