from fastmcp import FastMCP

mcp = FastMCP("My Math Server")


@mcp.tool
def add(a: float, b: float) -> float:
    """
    Return the sum of two numbers.
    """
    return a + b


@mcp.tool
def subtract(a: float, b: float) -> float:
    """
    Return the difference between two numbers.
    """
    return a - b


# Create ASGI application
app = mcp.http_app()
