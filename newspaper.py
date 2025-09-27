import weaviate
from weaviate.classes.init import Auth
import os

weaviate_url = os.environ["WEAVIATE_URL"]
weaviate_api_key = os.environ["WEAVIATE_API_KEY"]
cohere_api_key = os.environ["COHERE_APIKEY"]

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=weaviate_url,
    auth_credentials=Auth.api_key(weaviate_api_key),
    headers={"X-Cohere-Api-Key": cohere_api_key},
)

newspaper = client.collections.use("Newspaper")

uuid = newspaper.data.insert(
    properties={
        "media_name": "The Financial Times",
        "title": "",
    }
)

print(uuid)