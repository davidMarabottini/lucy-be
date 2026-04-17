import os
from dotenv import load_dotenv
from app import create_app
from app.config.logger import configure_logging

load_dotenv()

app = create_app()

if __name__ == "__main__":
    configure_logging()
    host = os.getenv("FLASK_RUN_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_RUN_PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "1").lower() in ("1", "true", "yes")
    app.run(host=host, port=port, debug=debug)