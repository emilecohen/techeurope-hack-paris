# updated_weaviate_delete_fastapi.py
import os
from contextlib import asynccontextmanager

import weaviate
from weaviate.classes.init import Auth
from dotenv import load_dotenv

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

from weaviate.classes.query import MetadataQuery, Filter

load_dotenv()

weaviate_url = os.getenv("WEAVIATE_URL")
weaviate_api_key = os.environ["WEAVIATE_API_KEY"]


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # ----- Client & auth -----
#     client = weaviate.connect_to_weaviate_cloud(
#         cluster_url=weaviate_url,
#         auth_credentials=Auth.api_key(weaviate_api_key),
#         # headers={"X-Cohere-Api-Key": os.environ.get("COHERE_APIKEY")},
#     )
#     app.state.weaviate = client
#     try:
#         yield
#     finally:
#         client.close()

app = FastAPI(title="updated_weaviate_delete")


# ------ receiving a uuid (as raw text) -------------
@app.post("/save")
async def save(text: str):
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=weaviate_url,
        auth_credentials=Auth.api_key(weaviate_api_key),
        # headers={"X-Cohere-Api-Key": os.environ.get("COHERE_APIKEY")},
    )
    # newspaper = client.collections.use("Newspaper")
    # jeopardy = client.collections.use("Newspaper")

    collection = client.collections.use("Newspaper")
    collection.data.delete_many(where=Filter.by_property("media_name").like(text))

    response = collection.query.near_text(
        query=" yyyy",
        limit=2,
        return_metadata=MetadataQuery(distance=True),
        filters=Filter.by_property("media_name").equal(text),
    )
    client.close()
    if response.objects == []:
        return "register is deleted correctly"
    else:
        return "something went"


@app.get("/save")
async def save():
    return f"Got hello"
