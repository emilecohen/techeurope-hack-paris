from flask import jsonify
from parser.fetcher import latest_articles, all_fetched_articles

def register_routes(app):

    @app.route("/articles", methods=["GET"])
    def get_articles():
        return jsonify(latest_articles)

    @app.route("/all_articles", methods=["GET"])
    def get_all_articles():
        return jsonify(all_fetched_articles)
