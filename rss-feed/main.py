from flask import Flask, jsonify
import feedparser
from dataclasses import dataclass, asdict
from typing import List
from datetime import datetime
import threading
import time

app = Flask(__name__)

@dataclass
class ArticleDataFrame:
    media_name: str
    title: str
    description: str
    author: str
    date: str  # ISO 8601 format
    language: str
    categories: List[str]
    newspaper_link: str
    rss_link: str
    rss_last_build: str  # ISO 8601 format
    #content: str
latest_articles = []

def fetch_rss_feed(rss_url: str) -> List[ArticleDataFrame]:
    feed = feedparser.parse(rss_url)
    articles = []

    rss_last_build = (
        datetime.utcnow().isoformat() + "Z"
        if not feed.get("feed", {}).get("updated_parsed")
        else datetime(*feed.feed.updated_parsed[:6]).isoformat() + "Z"
    )
    media_name = feed.feed.get("title", "Unknown Source")
    newspaper_link = feed.feed.get("link", rss_url)
    language = feed.feed.get("language", "unknown")

    for entry in feed.entries:
        pub_date = (
            datetime.utcnow().isoformat() + "Z"
            if not entry.get("published_parsed")
            else datetime(*entry.published_parsed[:6]).isoformat() + "Z"
        )

        article = ArticleDataFrame(
            media_name=media_name,
            title=entry.get("title", "No Title"),
            description=entry.get("summary", ""),
            author=entry.get("author", "Unknown"),
            date=pub_date,
            language=language,
            categories=entry.get("tags", []),
            newspaper_link=newspaper_link,
            rss_link=rss_url,
            rss_last_build=rss_last_build,
            #content=entry.get("content", [{}])[0].get("value", entry.get("summary", "")),
        )

        if isinstance(article.categories, list):
            article.categories = [
                tag["term"] for tag in article.categories if isinstance(tag, dict)
            ]

        articles.append(article)

    return articles


def auto_fetch_rss():
    global latest_articles
    rss_urls = rss_urls = [
    "http://rss.cnn.com/rss/cnn_topstories.rss",          # CNN - Top Stories
    "http://feeds.nytimes.com/nyt/rss/HomePage",          # The New York Times - Home
    "https://feeds.bbci.co.uk/news/world/rss.xml",        # BBC News - World
    "https://feeds.reuters.com/reuters/topNews",          # Reuters - Top News
    "http://www.npr.org/rss/rss.php?id=1001",             # NPR News
    "https://www.aljazeera.com/xml/rss/all.xml",          # Al Jazeera - All News
    "https://techcrunch.com/feed/",                       # TechCrunch
    "https://www.theguardian.com/world/rss",              # The Guardian - World
    "https://www.wired.com/feed/rss",                     # Wired
    "https://www.bloomberg.com/feed/podcast/bloomberg-surveillance.xml", # Bloomberg
    "https://www.forbes.com/real-time/feed2",             # Forbes
    "https://www.ft.com/?format=rss",                     # Financial Times
    ]

    while True:
        all_articles = []
        for rss_url in rss_urls:
            articles = fetch_rss_feed(rss_url)
            all_articles.extend([asdict(article) for article in articles])

        latest_articles = all_articles
        print(f"Articles: {all_articles}")
        time.sleep(30)

@app.route("/articles", methods=["GET"])
def get_articles():
    return jsonify(latest_articles)


if __name__ == "__main__":
    threading.Thread(target=auto_fetch_rss, daemon=True).start()
    app.run(debug=True, port=5000)
