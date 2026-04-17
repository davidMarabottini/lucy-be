import os

from flask import send_from_directory


def register_spa_routes(app):
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def catch_all(path):
        file_path = os.path.join(app.static_folder, path)
        if path and os.path.exists(file_path):
            return send_from_directory(app.static_folder, path)
        if path.startswith("api/"):
            return {"error": "API non trovata"}, 404
        return send_from_directory(app.static_folder, "index.html")
