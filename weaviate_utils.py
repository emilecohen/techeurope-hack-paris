import os
import weaviate
from weaviate.auth import AuthApiKey
from weaviate.classes.query import MetadataQuery

weaviate_api_key = os.environ["WEAVIATE_API_KEY"]
weaviate_url = os.environ["WEAVIATE_URL"]

def connect_to_weaviate():
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=weaviate_url,
        auth_credentials=AuthApiKey(api_key=weaviate_api_key),
    )
    print(client)
    return client


def get_articles(client, query, limit):
    from weaviate.classes.query import Filter

    newspaper = client.collections.use("Newspaper")
    response = newspaper.query.near_text(
    query=query,
    limit=limit,
    return_metadata=MetadataQuery(distance=True)
)

    for o in response.objects:
        print(o.properties)
    
    return response.objects


if __name__ == "__main__":
    client = connect_to_weaviate()
    articles = get_articles(client, "animals in movies", 2)
    print(articles)