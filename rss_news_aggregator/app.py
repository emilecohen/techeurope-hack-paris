from flask import Flask, jsonify
from parser.fetcher import all_fetched_articles, latest_articles, auto_fetch_rss

app = Flask(__name__)

@app.route("/articles", methods=["GET"])
def get_articles():
    return jsonify(latest_articles)

@app.route("/all_articles", methods=["GET"])
def get_all_articles():
    return jsonify(all_fetched_articles)

@app.route("/fetch", methods=["GET"])
def fetch_articles():
    auto_fetch_rss(max_articles=50)
    return jsonify({"status": "success", "fetched": len(latest_articles)})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
