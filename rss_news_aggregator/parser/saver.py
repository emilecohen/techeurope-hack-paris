import json
import os
from types import SimpleNamespace
from typing import List

from dotenv import load_dotenv

import weaviate
from weaviate.classes.init import Auth

# Load the .env file
load_dotenv()

# Access environment variables
weaviate_url = os.getenv("WEAVIATE_URL")
weaviate_api_key = os.getenv("WEAVIATE_API_KEY")
cohere_api_key = os.getenv("COHERE_API_KEY")

def save_articles_to_db(articles: List[dict]):
    print("something here")
    try:
        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=weaviate_url,
            auth_credentials=Auth.api_key(weaviate_api_key),
            headers={"X-Cohere-Api-Key": cohere_api_key},
        )

        print(client)

        newspaper = client.collections.use("Newspaper")

        with newspaper.batch.fixed_size(batch_size=200) as batch:
            for data_row in articles:
                batch.add_object(
                    {
                        "media_name": data_row["media_name"],
                        "title": data_row["title"],
                        "description": data_row["description"],
                        "author": data_row["author"],
                        "date": data_row["date"],
                        "language": data_row["language"],
                        "categories": data_row["categories"],
                        "newspaper_link": data_row["newspaper_link"],
                        "rss_link": data_row["rss_link"],
                        "rss_last_build": data_row["rss_last_build"],
                        "content": data_row["content"]
                    }
                )

                if batch.number_errors > 10:
                    print("Batch import stopped due to excessive errors.")
                    break

    except Exception as e:
        print(f"There has been an error connecting to weaviate: {e}")
    
    finally:
        client.close()

"""
def save_articles_to_json(articles: List[dict], filename="data/all_articles.json"):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(articles, f, indent=4, ensure_ascii=False)
        print(f"Saved {len(articles)} articles to {filename}")
    except Exception as e:
        print(f"Failed to save articles to JSON: {e}")
"""
