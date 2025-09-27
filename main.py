"""
MCP Server Template
"""

from mcp.server.fastmcp import FastMCP
from pydantic import Field
from typing import Optional

import mcp.types as types

from weaviate_utils import connect_to_weaviate, get_articles

templates = """Truth. It’s more important now than ever.
Established 1851.

IDENTITY:
We are a global leader in independent journalism, dedicated to seeking the truth and helping people understand the world. Our role is to inform, inspire, and empower our community through rigorous reporting, in-depth analysis, and a steadfast commitment to integrity.

VOICE:
Speak in a clear, authoritative, and thoughtful manner. We address readers with respect, clarity, and a sense of shared purpose. Always use "we" for the newspaper and "our" for the community.

STYLE EXAMPLES:
- "Our mission is to seek the truth and help people understand the world."
- "Breaking news that doesn’t sacrifice quality for speed."
- "Expert beat reporting that allows readers to stay abreast of important subjects and storylines."

CONTENT FOCUS:
Prioritize national and international news, politics, culture, science, business, technology, opinion, and investigative reporting. Always uphold accuracy, fairness, and depth in every story.

INTERACTION:
Greet with "Welcome to The New York Times." When discussing news, present stories with context and nuance. Offer to go deeper by saying "Would you like a more detailed analysis or related perspectives?"
"""

mcp = FastMCP("Newspaper Agent", stateless_http=True)


@mcp.tool(
    title="Get Articles",
    description="Get articles from Weaviate with config instructions",
)
def get_articles_with_config(
    query: str = Field(description="Search query for articles"),
) -> str:
    """Get articles with config instructions prepended"""
    try:

        # Connect to Weaviate and get articles
        client = connect_to_weaviate()
        articles = get_articles(client, query, limit=5)

        media_names = []
        cats = []

        for art in articles:
            media_names.append(art.properties["media_name"])
            cats.append(art.properties["categories"])

        main_cats = set(cat for sublist in cats for cat in sublist)
        unique_media_names = set(media_names)

        response = f"Newspapers: {unique_media_names}\n\n"
        response += f"Categories:\n{main_cats}\n\n"
        response += f"Instructions:\n{templates}\n\n"
        response += "=" * 50 + "\n"
        response += f"ARTICLES (Query: '{query}', Limit: {5})\n"
        response += "=" * 25 + "\n\n"

        if not articles:
            response += "No articles found for the given query."
        else:
            for i, article in enumerate(articles, 1):
                response += f"Article {i}:\n"
                response += f"Title: {article.properties.get('title', 'N/A')}\n"
                response += f"Media Name: {article.properties.get("media_name","N/A")}"
                response += f"Content: {article.properties.get('content', 'N/A')}\n"
                response += f"URL: {article.properties.get('url', 'N/A')}\n"
                response += (
                    f"Published: {article.properties.get('published_date', 'N/A')}\n"
                )
                if hasattr(article, "metadata") and article.metadata.distance:
                    response += (
                        f"Relevance Score: {1 - article.metadata.distance:.3f}\n"
                    )
                response += "\n" + "-" * 40 + "\n\n"

        client.close()

        return response

    except Exception as e:
        return f"Error retrieving articles: {str(e)}"
    finally:
        client.close()


@mcp.tool()
def temp() -> str:
    return "Bye"


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
