from flask import Flask, jsonify
import feedparser
from dataclasses import dataclass, asdict
from typing import List
from datetime import datetime, timezone
from bs4 import BeautifulSoup
import requests
import json

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

latest_articles: List[dict] = []
all_fetched_articles: List[dict] = []

# ------------------------
# Helper Functions
# ------------------------

def clean_html(raw_html: str) -> str:
    if not raw_html:
        return ""
    try:
        return BeautifulSoup(raw_html, "html.parser").get_text().strip()
    except Exception as e:
        print(f"Failed to clean HTML: {e}")
        return raw_html

def fetch_article_content(url: str) -> str:
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        paragraphs = soup.find_all("p")
        return "\n".join(p.get_text().strip() for p in paragraphs if p.get_text().strip())
    except Exception as e:
        print(f"Failed to fetch article content from {url}: {e}")
        return ""

def format_datetime(parsed_struct=None) -> str:
    """Convert a struct_time or None to RFC3339 UTC string."""
    if parsed_struct:
        return datetime(*parsed_struct[:6], tzinfo=timezone.utc).isoformat(timespec='seconds') + "Z"
    return datetime.utcnow().replace(tzinfo=timezone.utc).isoformat(timespec='seconds') + "Z"

def fetch_rss_feed(rss_url: str) -> List[ArticleDataFrame]:
    try:
        feed = feedparser.parse(rss_url)
    except Exception as e:
        print(f"Failed to parse RSS feed {rss_url}: {e}")
        return []

    articles = []
    try:
        rss_last_build = format_datetime(feed.feed.get("updated_parsed"))
        media_name = feed.feed.get("title", "Unknown Source")
    except Exception as e:
        print(f"Failed to extract feed metadata for {rss_url}: {e}")
        rss_last_build = format_datetime()
        media_name = "Unknown Source"

    for entry in feed.entries:
        try:
            pub_date = format_datetime(entry.get("published_parsed"))
            description = clean_html(entry.get("summary", ""))
            newspaper_link = entry.get("link", rss_url)
            content = fetch_article_content(newspaper_link)

            if not description and not content:
                continue

            categories = entry.get("tags", [])
            if isinstance(categories, list):
                categories = [clean_html(tag["term"]) for tag in categories if isinstance(tag, dict)]
            else:
                categories = []

            article = ArticleDataFrame(
                media_name=media_name,
                title=clean_html(entry.get("title", "No Title")),
                description=description,
                author=clean_html(entry.get("author", "Unknown")),
                date=pub_date,
                language=feed.feed.get("language", "unknown"),
                categories=categories,
                newspaper_link=newspaper_link,
                rss_link=rss_url,
                rss_last_build=rss_last_build,
                content=content,
            )

            articles.append(article)

        except Exception as e:
            print(f"Failed to process article from {rss_url}: {e}")
            continue

    return articles

def save_articles_to_json(articles: List[dict], filename="articles.json"):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(articles, f, indent=4, ensure_ascii=False)
        print(f"Saved {len(articles)} articles to {filename}")
    except Exception as e:
        print(f"Failed to save articles to JSON: {e}")

# ------------------------
# Refactored Auto-fetching
# ------------------------

def auto_fetch_rss(max_articles=50):
    """
    Fetch RSS feeds until max_articles are collected, avoiding duplicates.
    """
    global latest_articles, all_fetched_articles
    rss_urls = [
        "https://feeds.bbci.co.uk/news/world/rss.xml",
        "https://www.aljazeera.com/xml/rss/all.xml",
        "https://www.theguardian.com/world/rss",
        "https://feeds.reuters.com/Reuters/worldNews",
        "https://www.cfr.org/rss/news-releases.xml",
        "https://worldview.stratfor.com/feed",
        "https://www.defenseone.com/feeds/all/",
        "https://carnegieendowment.org/rss/news"
    ]

    new_articles = []

    for rss_url in rss_urls:
        if len(all_fetched_articles) >= max_articles:
            break
        try:
            articles = fetch_rss_feed(rss_url)
            for article in articles:
                dict_article = asdict(article)
                # Avoid duplicates by newspaper link
                if dict_article['newspaper_link'] in [a['newspaper_link'] for a in all_fetched_articles]:
                    continue

                new_articles.append(dict_article)
                all_fetched_articles.append(dict_article)

                # ✅ Print when max_articles is reached
                if len(all_fetched_articles) >= max_articles:
                    print("✅ Max articles reached!")
                    break
            if len(all_fetched_articles) >= max_articles:
                break
        except Exception as e:
            print(f"Error fetching from {rss_url}: {e}")
            continue

    latest_articles = new_articles
    save_articles_to_json(all_fetched_articles, "all_articles.json")
    print(f"Fetched {len(new_articles)} new articles. Total: {len(all_fetched_articles)}")

# ------------------------
# Flask Routes
# ------------------------

@app.route("/articles", methods=["GET"])
def get_articles():
    return jsonify(latest_articles)

@app.route("/all_articles", methods=["GET"])
def get_all_articles():
    return jsonify(all_fetched_articles)

# ------------------------
# Main
# ------------------------

if __name__ == "__main__":
    auto_fetch_rss(max_articles=50)
    app.run(debug=True, port=5000, use_reloader=False)
