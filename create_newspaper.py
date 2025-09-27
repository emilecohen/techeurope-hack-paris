# updated_weaviate_import.py
import os
import weaviate
from weaviate.classes.init import Auth
import os

# ----- Client & auth -----
weaviate_url = os.environ["WEAVIATE_URL"]
weaviate_api_key = os.environ["WEAVIATE_API_KEY"]
cohere_api_key = os.environ["COHERE_APIKEY"]

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=weaviate_url,
    auth_credentials=Auth.api_key(weaviate_api_key),
    headers={"X-Cohere-Api-Key": cohere_api_key},
)

# ----- Schema: updated and cleaned -----
collection_name = 'Newspaper'

movie_class_schema = {
    "class": collection_name,
    "description": "A collection of movies since 1970.",
    # Use the OpenAI module to vectorize text properties
    "vectorizer": "text2vec-openai", # A changer
    # Vector index config (HNSW is default; set search distance and ef tuning)
    "vectorIndexConfig": {
        "distance": "cosine",
        "ef": 128
    },
    # Module config for the text2vec-openai module:
    "moduleConfig": {
        "text2vec-openai": {
            # Use a modern OpenAI embedding model
            "model": "text-embedding-3-large",
            "type": "text",
            # don't vectorize the class name itself (optional)
            "vectorizeClassName": False
        }
    },
    "properties": [
        # numeric / ids: skip vectorization
        {
            "name": "newspaper_id",
            "dataType": ["number"],
            "description": "The id of the newspaper",
            "moduleConfig": {
                "text2vec-openai": {
                    "skip": True,
                    "vectorizePropertyName": False
                }
            }
        },
        # title: you may want title searchable via text, but many use-cases prefer to NOT rely on embedding for titles.
        # We'll keep title in text (not vectorized) because main semantic search will use 'description'/'plot'.
        {
            "name": "title",
            "dataType": ["text"],
            "description": "The name of the newspaper",
            "moduleConfig": {
                "text2vec-openai": {
                    "skip": True,
                    "vectorizePropertyName": False
                }
            }
        },
        {
            "name": "year",
            "dataType": ["number"],
            "description": "The year in which movie was published",
            "moduleConfig": {
                "text2vec-openai": {
                    "skip": True,
                    "vectorizePropertyName": False
                }
            }
        },
        # poster link/url: skip embeddings
        {
            "name": "poster_link",
            "dataType": ["text"],
            "description": "The poster link of the movie",
            "moduleConfig": {
                "text2vec-openai": {
                    "skip": True,
                    "vectorizePropertyName": False
                }
            }
        },
        # genres/actors/director: store as text but skip vectorization (you may instead treat these as structured fields)
        {
            "name": "genres",
            "dataType": ["text"],
            "description": "The genres of the movie",
            "moduleConfig": {
                "text2vec-openai": {
                    "skip": True,
                    "vectorizePropertyName": False
                }
            }
        },
        {
            "name": "actors",
            "dataType": ["text"],
            "description": "The actors of the movie",
            "moduleConfig": {
                "text2vec-openai": {
                    "skip": True,
                    "vectorizePropertyName": False
                }
            }
        },
        {
            "name": "director",
            "dataType": ["text"],
            "description": "Director of the movie",
            "moduleConfig": {
                "text2vec-openai": {
                    "skip": True,
                    "vectorizePropertyName": False
                }
            }
        },
        # description & plot: these are the main semantic fields -> allow vectorization
        {
            "name": "description",
            "dataType": ["text"],
            "description": "Overview / description of the movie"
        },
        {
            "name": "plot",
            "dataType": ["text"],
            "description": "Plot of the movie from Wikipedia"
        },
        # keywords: small short tokens — keep as text but skip vectorization (choice; if you want keywords to influence semantic search,
        # set skip=False)
        {
            "name": "keywords",
            "dataType": ["text"],
            "description": "main keywords of the movie",
            "moduleConfig": {
                "text2vec-openai": {
                    "skip": True,
                    "vectorizePropertyName": False
                }
            }
        }
    ]
}

client.schema.create_class(movie_class_schema)

# ----- Batch import: configure and use context manager for robust writes -----
client.batch.configure(batch_size=50, dynamic=True, timeout_retries=3)

with client.batch as batch:
    # add objects in batches (uses batch.add_data_object internally)
    for i in tqdm(range(len(df)), desc="Importing movies"):
        item = df.iloc[i]
        obj = {
            "movie_id": float(item['id']),
            "title": str(item['Name']).strip(),
            "year": int(item['year']),
            "poster_link": str(item.get('PosterLink', '')),
            "genres": str(item.get('Genres', '')),
            "actors": str(item.get('Actors', '')),
            "director": str(item.get('Director', '')),
            "description": str(item.get('Description', '')),
            "plot": str(item.get('Plot', '')),
            "keywords": str(item.get('Keywords', ''))
        }
        # add data object to batch (the client will ask the module to vectorize allowed fields)
        try:
            batch.add_data_object(obj, collection_name)
        except Exception as e:
            print(f"Failed adding object idx={i}, id={item.get('id')} -> {e}")
            # optionally continue or break depending on how you want to handle failures
            continue

# Flush batch (context manager will flush at exit, but explicit flush is fine)
client.batch.flush()

# Quick sanity check: count objects
agg_res = client.query.aggregate(collection_name).with_meta_count().do()
print("Aggregate/count result:", agg_res)
