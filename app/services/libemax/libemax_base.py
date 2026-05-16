import os
import requests
import logging

from app.exception import APIError

logger = logging.getLogger(__name__)


class LibemaxBase:
    """Client base condiviso per tutte le API Libemax."""

    def __init__(self):
        self.api_key = os.getenv("LIBEMAX_API_KEY")
        self.base_url = os.getenv("LIBEMAX_BASE_URL")
        self.lang = "it"
        self.api_version = "v3"
        if not self.api_key:
            logger.warning("LIBEMAX_API_KEY non configurata nel file .env")
        if not self.base_url:
            logger.warning(
                "LIBEMAX_BASE_URL non configurata nel file .env. "
                "Formato atteso: https://{account}.libemax.com/app-timbrature"
            )

    def _post(self, endpoint: str, payload: dict = None):
        """POST form-urlencoded verso Libemax. Ritorna il contenuto di 'dati'."""
        if not self.api_key:
            raise APIError("LIBEMAX_API_KEY non configurata nel file .env", 500)
        if not self.base_url:
            raise APIError(
                "LIBEMAX_BASE_URL non configurata nel file .env. "
                "Formato: https://{account}.libemax.com/app-timbrature",
                500,
            )
        url = f"{self.base_url}/{self.lang}/api/{self.api_version}/{endpoint}"
        headers = {"x-api-key": self.api_key}

        logger.info("POST %s", url)
        resp = requests.post(url, data=payload or {}, headers=headers, timeout=30)
        logger.info("POST %s → %s", url, resp.status_code)

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

        logger.info("POST multipart %s", url)
        resp = requests.post(url, data=payload or {}, files=files or {}, headers=headers, timeout=60)
        logger.info("POST multipart %s → %s", url, resp.status_code)

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
