import os
import weaviate
from weaviate.auth import AuthApiKey
from weaviate.classes.query import MetadataQuery, Filter

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

    newspaper = client.collections.use("Newspaper")
    response = newspaper.query.near_text(
        query=query, limit=limit, return_metadata=MetadataQuery(distance=True)
    )

    for o in response.objects:
        print(o.properties)

    client.close()
    return response.objects


def delete_articles(client, media_name):
    collection = client.collections.use("Newspaper")
    collection.data.delete_many(where=Filter.by_property("media_name").like(media_name))

    response = collection.query.near_text(
        query=" ",
        limit=2,
        return_metadata=MetadataQuery(distance=True),
        filters=Filter.by_property("media_name").equal(media_name),
    )
    client.close()
    if response.objects == []:
        return "register is deleted correctly"
    else:
        return "something went"


if __name__ == "__main__":
    client = connect_to_weaviate()
    articles = get_articles(client, "animals in movies", 2)
    print(articles)
