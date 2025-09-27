import json
from typing import List

def save_articles_to_json(articles: List[dict], filename="data/all_articles.json"):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(articles, f, indent=4, ensure_ascii=False)
        print(f"Saved {len(articles)} articles to {filename}")
    except Exception as e:
        print(f"Failed to save articles to JSON: {e}")
