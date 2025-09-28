from dataclasses import asdict
from datetime import datetime, timezone
from typing import List

import feedparser
from models.articles import ArticleDataFrame

from .cleaner import clean_html, fetch_article_content
from .saver import save_articles_to_db

latest_articles: List[dict] = []
all_fetched_articles: List[dict] = []

def format_datetime(parsed_struct=None) -> str:
    """Convert a struct_time or None to RFC3339 UTC string."""
    if parsed_struct:
        # Convert struct_time or tuple to datetime in UTC
        dt = datetime(*parsed_struct[:6], tzinfo=timezone.utc)
    else:
        dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    
    # Return RFC3339 format with 'Z' for UTC
    return dt.isoformat(timespec='seconds').replace('+00:00', 'Z')

def fetch_rss_feed(company_name: str, language: str, rss_url: str) -> List[ArticleDataFrame]:
    """
    Fetches and parses a single RSS feed URL and returns a list of ArticleDataFrame objects.
    """
    try:
        feed = feedparser.parse(rss_url)
    except Exception as e:
        print(f"Failed to parse RSS feed {rss_url}: {e}")
        return []

    articles = []
    rss_last_build = format_datetime(feed.feed.get("updated_parsed"))
    media_name = company_name
    language = language

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
                language=language,
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

# ------------------------
# Auto-fetch Function
# ------------------------

def auto_fetch_rss(company_name: str, language: str, max_articles: int, rss_link: str):
    """
    Fetch RSS feed from a single RSS link until max_articles are collected, avoiding duplicates.
    """
    global latest_articles, all_fetched_articles

    new_articles = []

    print(rss_link)

    if len(all_fetched_articles) >= max_articles:
        return

    try:
        articles = fetch_rss_feed(company_name, language, rss_link)
        for article in articles:
            dict_article = asdict(article)
            # Avoid duplicates by newspaper link
            if dict_article['newspaper_link'] in [a['newspaper_link'] for a in all_fetched_articles]:
                continue

            new_articles.append(dict_article)
            all_fetched_articles.append(dict_article)

            if len(all_fetched_articles) >= max_articles:
                break

    except Exception as e:
        print(f"Error fetching from {rss_link}: {e}")

    latest_articles = new_articles
    save_articles_to_db(all_fetched_articles)
    print(f"Fetched {len(new_articles)} new articles. Total: {len(all_fetched_articles)}")

