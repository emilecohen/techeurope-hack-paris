from app import create_app
from parser.fetcher import auto_fetch_rss

app = create_app()

if __name__ == "__main__":
    auto_fetch_rss(max_articles=50)
    app.run(debug=True, port=5000, use_reloader=False)
