from flask import Flask, jsonify
import feedparser
from dataclasses import dataclass, asdict
from typing import List
from datetime import datetime
import threading
import time
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@dataclass
class ArticleDataFrame:
    media_name: str
    title: str
    description: str
    author: str
    date: str  # RFC 3339 format
    language: str
    categories: List[str]
    newspaper_link: str
    rss_link: str
    rss_last_build: str  # RFC 3339 format
    content: str

latest_articles = []
all_fetched_articles = []  # ✅ Keep all successfully fetched articles

# Helper to strip HTML + decode entities
def clean_html(raw_html: str) -> str:
    if not raw_html:
        return ""
    return BeautifulSoup(raw_html, "html.parser").get_text().strip()

def fetch_article_content(url: str) -> str:
    """Fetch full article content from the webpage."""
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        paragraphs = soup.find_all("p")
        return "\n".join(p.get_text().strip() for p in paragraphs if p.get_text().strip())
    except Exception as e:
        print(f"Failed to fetch article content from {url}: {e}")
        return ""

def fetch_rss_feed(rss_url: str) -> List[ArticleDataFrame]:
    feed = feedparser.parse(rss_url)
    articles = []

    rss_last_build = (
        datetime.utcnow().isoformat(timespec='seconds') + "Z"
        if not feed.get("feed", {}).get("updated_parsed")
        else datetime(*feed.feed.updated_parsed[:6]).isoformat(timespec='seconds') + "Z"
    )
    media_name = feed.feed.get("title", "Unknown Source")

    for entry in feed.entries:
        pub_date = (
            datetime.utcnow().isoformat(timespec='seconds') + "Z"
            if not entry.get("published_parsed")
            else datetime(*entry.published_parsed[:6]).isoformat(timespec='seconds') + "Z"
        )

        description = clean_html(entry.get("summary", ""))
        newspaper_link = entry.get("link", rss_url)
        content = fetch_article_content(newspaper_link)

        if not description and not content:
            continue

        article = ArticleDataFrame(
            media_name=media_name,
            title=clean_html(entry.get("title", "No Title")),
            description=description,
            author=clean_html(entry.get("author", "Unknown")),
            date=pub_date,
            language=feed.feed.get("language", "unknown"),
            categories=entry.get("tags", []),
            newspaper_link=newspaper_link,
            rss_link=rss_url,
            rss_last_build=rss_last_build,
            content=content,
        )

        if isinstance(article.categories, list):
            article.categories = [
                clean_html(tag["term"]) for tag in article.categories if isinstance(tag, dict)
            ]

        articles.append(article)

    return articles

def auto_fetch_rss():
    global latest_articles, all_fetched_articles
    rss_urls = [
        "https://feeds.bbci.co.uk/news/world/rss.xml",
        "https://www.aljazeera.com/xml/rss/all.xml",
        "https://www.theguardian.com/world/rss",
        "https://feeds.reuters.com/Reuters/worldNews",
        "https://foreignpolicy.com/feed/",
        "https://www.cfr.org/rss/news-releases.xml",
        "https://worldview.stratfor.com/feed",
        "https://www.defenseone.com/feeds/all/",
        "https://thediplomat.com/feed/",
        "https://carnegieendowment.org/rss/news"
    ]

    while True:
        all_articles = []
        for rss_url in rss_urls:
            articles = fetch_rss_feed(rss_url)
            dict_articles = [asdict(article) for article in articles]
            all_articles.extend(dict_articles)

            # Append new articles to cumulative list (avoid duplicates)
            for article in dict_articles:
                if article not in all_fetched_articles:
                    all_fetched_articles.append(article)

        latest_articles = all_articles

        # Print preview of first 3 articles
        print("\n=== Sample Articles ===")
        for row in latest_articles[:3]:
            print(f"[{row['media_name']}] {row['title']}")
            print(f"Author: {row['author']}")
            print(f"Description: {row['description'][:]}")
            print(f"Content: {row['content'][:]}\n")

        time.sleep(30)

@app.route("/articles", methods=["GET"])
def get_articles():
    """Return latest fetched articles."""
    return jsonify(latest_articles)

@app.route("/all_articles", methods=["GET"])
def get_all_articles():
    """Return all successfully fetched articles since server start."""
    return jsonify(all_fetched_articles)

if __name__ == "__main__":
    threading.Thread(target=auto_fetch_rss, daemon=True).start()
    app.run(debug=True, port=5000)
