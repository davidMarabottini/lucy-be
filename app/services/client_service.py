from app.auth.decorators import paginated_response

from ..models import Client, db

class ClientService:
    @staticmethod
    @paginated_response
    def get_all():
        return Client.query

    @staticmethod
    def get_by_id(client_id):
        return db.session.get(Client, client_id)

    @staticmethod
    def create(data):
        client = Client(
            name=data.get("name"),
            email=data.get("email"),
            phone=data.get("phone"),
            # domain_id=data.get("domain_id"),
        )
        db.session.add(client)
        db.session.commit()
        return client

    @staticmethod
    def update(client_id, data):
        client = Client.query.get(client_id)
        if not client:
            return None

        if "name" in data: client.name = data["name"]
        if "email" in data: client.email = data["email"]
        if "phone" in data: client.phone = data["phone"]

        db.session.commit()
        return client

    @staticmethod
    def delete(client_id):
        client = Client.query.get(client_id)
        if not client:
            return False

        db.session.delete(client)
        db.session.commit()
        return True
