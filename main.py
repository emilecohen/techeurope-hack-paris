"""
MCP Server Template
"""

from mcp.server.fastmcp import FastMCP
from pydantic import Field
from typing import Optional

import mcp.types as types
from agent_config_utils import get_agent_instructions, get_default_agent_config
from constants import AGENT_CONFIG_ID
from weaviate_utils import connect_to_weaviate, get_articles

mcp = FastMCP("Newspaper Agent", stateless_http=True)


@mcp.tool(
    title="Get Config Instructions",
    description="Get agent configuration instructions for writing articles",
)
def get_config_instructions(
    config_id: Optional[str] = Field(description="Config ID to retrieve (uses default if not provided)", default=None)
) -> str:
    """Get agent configuration instructions"""
    try:
        # Handle case where FastMCP might pass Field description as value
        if config_id is None:
            result = get_agent_instructions()
        else:
            result = get_agent_instructions(config_id)
        
        if result["status"] == "success":
            return f"Newspaper: {result['newspaper_name']}\n\nInstructions:\n{result['instructions']}"
        else:
            return f"Error: {result['error']}"
    except Exception as e:
        return f"Error retrieving config instructions: {str(e)}"


@mcp.tool(
    title="Get Articles",
    description="Get articles from Weaviate with config instructions",
)
def get_articles_with_config(
    query: str = Field(description="Search query for articles"),
    limit: int = Field(description="Number of articles to return", default=5),
    config_id: Optional[str] = Field(description="Config ID to retrieve (uses default if not provided)", default=None)
) -> str:
    """Get articles with config instructions prepended"""
    try:
        # Get config instructions first
        # Handle case where FastMCP might pass Field description as value
        if config_id is None or str(config_id).startswith("annotation="):
            config_result = get_agent_instructions()
        else:
            config_result = get_agent_instructions(config_id)
        
        if config_result["status"] != "success":
            return f"Error getting config: {config_result['error']}"
        
        # Connect to Weaviate and get articles
        client = connect_to_weaviate()
        articles = get_articles(client, query, limit)
        
        # Format response
        response = f"Newspaper: {config_result['newspaper_name']}\n\n"
        response += f"Instructions:\n{config_result['instructions']}\n\n"
        response += "=" * 50 + "\n"
        response += f"ARTICLES (Query: '{query}', Limit: {limit})\n"
        response += "=" * 50 + "\n\n"
        
        if not articles:
            response += "No articles found for the given query."
        else:
            for i, article in enumerate(articles, 1):
                response += f"Article {i}:\n"
                response += f"Title: {article.properties.get('title', 'N/A')}\n"
                response += f"Content: {article.properties.get('content', 'N/A')}\n"
                response += f"URL: {article.properties.get('url', 'N/A')}\n"
                response += f"Published: {article.properties.get('published_date', 'N/A')}\n"
                if hasattr(article, 'metadata') and article.metadata.distance:
                    response += f"Relevance Score: {1 - article.metadata.distance:.3f}\n"
                response += "\n" + "-" * 40 + "\n\n"
        
        client.close()
        return response
        
    except Exception as e:
        return f"Error retrieving articles: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
