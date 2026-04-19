import os
import requests
import logging

from app.exception import APIError

logger = logging.getLogger(__name__)


class LibemaxBase:
    """Client base condiviso per tutte le API Libemax."""

    def __init__(self):
        self.api_key = os.getenv("LIBEMAX_API_KEY")
        self.base_url = os.getenv("LIBEMAX_BASE_URL", "https://app.libemax.com")
        self.lang = "it"
        self.api_version = "v3"

    def _post(self, endpoint: str, payload: dict = None):
        """POST form-urlencoded verso Libemax. Ritorna il contenuto di 'dati'."""
        url = f"{self.base_url}/{self.lang}/api/{self.api_version}/{endpoint}"
        headers = {"x-api-key": self.api_key}

        resp = requests.post(url, data=payload or {}, headers=headers, timeout=30)

        if resp.status_code == 401:
            raise APIError("API key Libemax non valida", 401)
        if resp.status_code != 200:
            logger.error("Libemax %s returned %s", endpoint, resp.status_code)
            raise APIError(f"Errore Libemax: {resp.status_code}", 502)

        body = resp.json()
        if body.get("ritorno") != 1:
            msgs = body.get("messaggi", [])
            raise APIError(f"Errore Libemax: {msgs}", 400)

        return body.get("dati", {})

    def _post_multipart(self, endpoint: str, payload: dict = None, files: dict = None):
        """POST multipart/form-data verso Libemax (usato per upload documenti)."""
        url = f"{self.base_url}/{self.lang}/api/{self.api_version}/{endpoint}"
        headers = {"x-api-key": self.api_key}

        resp = requests.post(url, data=payload or {}, files=files or {}, headers=headers, timeout=60)

        if resp.status_code == 401:
            raise APIError("API key Libemax non valida", 401)
        if resp.status_code != 200:
            logger.error("Libemax %s returned %s", endpoint, resp.status_code)
            raise APIError(f"Errore Libemax: {resp.status_code}", 502)

        body = resp.json()
        if body.get("ritorno") != 1:
            msgs = body.get("messaggi", [])
            raise APIError(f"Errore Libemax: {msgs}", 400)

        return body.get("dati", {})
