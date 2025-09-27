from dataclasses import dataclass
from typing import List

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
