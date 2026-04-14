import os
from openapi_lrp.api_pubbliche_libemax_client import AuthenticatedClient

from openapi_lrp.api_pubbliche_libemax_client.api.cliente import (
    post_lang_api_api_version_cliente_cliente_elenco
)
from openapi_lrp.api_pubbliche_libemax_client.models.response_cliente_elenco import ResponseClienteElenco
from ...models import db, Client
import logging

class LibemaxClientService:
    def __init__(self):
        self.api_key = os.getenv("DISINFEKTMI_LIBEMAX_API_KEY")
        self.base_url = os.getenv("LIBEMAX_BASE_URL", "https://api.libemax.com")
        self.default_lang = "it"
        self.api_version = "3.0"

    def _get_client(self):
        return AuthenticatedClient(
            base_url=self.base_url, 
            token=self.api_key,
            prefix="x-api-key",
            auth_header_name="x-api-key"
        )

    def sync_clients(self):
        logging.info("Inizio sincronizzazione clienti")
        client = self._get_client()
        json_body = {}
        
        # json_body = RequestClienteElenco()
        
        response = post_lang_api_api_version_cliente_cliente_elenco.sync_detailed(
            client=client,
            lang=self.default_lang,
            api_version=self.api_version,
            json_body=json_body
        )

        if response.status_code != 200:
            logging.error(f"Errore API Libemax: {response.status_code}")
            return 0, f"Libemax API Error: {response.status_code}"

        parsed: ResponseClienteElenco = response.parsed
        if not parsed or parsed.ritorno != 1:
            logging.warning("Errore nel parsing dei dati o esito negativo")
            return 0, "Errore nel parsing dei dati o esito negativo"

        remote_clients = parsed.dati if hasattr(parsed, 'dati') else []
        new_count = 0

        for r_client in remote_clients:
            if not Client.query.filter_by(libemax_id=r_client.id).first():
                new_client = Client(
                    name=r_client.ragione_sociale,
                    libemax_id=r_client.id,
                    email=getattr(r_client, 'email', None)
                )
                db.session.add(new_client)
                new_count += 1
        
        db.session.commit()
        logging.info("Clienti aggiornati")
        return new_count, None