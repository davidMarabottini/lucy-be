from sqlalchemy import inspect

class BaseModel:
    def to_dict(self, seen_ids=None):
        if seen_ids is None:
            seen_ids = set()

        # Identificativo per evitare cicli
        obj_id = (self.__class__.__name__, getattr(self, 'id', id(self)))
        if obj_id in seen_ids:
            return {"id": getattr(self, 'id', None)}
        
        seen_ids.add(obj_id)

        # 1. Partiamo dalle colonne fisiche della tabella (base)
        data = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

        # 2. Esploriamo SOLO ciò che è presente nel dizionario interno dell'oggetto.
        # SQLAlchemy mette nel __dict__ le relazioni solo se sono state caricate (Eager Loading).
        internal_data = self.__dict__
        
        for key, value in internal_data.items():
            # Saltiamo gli attributi interni di SQLAlchemy (iniziano con _)
            if key.startswith('_'):
                continue
            
            # Se il valore è un'altra istanza BaseModel (relazione singola)
            if hasattr(value, 'to_dict'):
                data[key] = value.to_dict(seen_ids=seen_ids.copy())
            
            # Se il valore è una lista di oggetti (relazione collection)
            elif isinstance(value, list):
                # Verifichiamo se gli elementi della lista sono modelli serializzabili
                if value and hasattr(value[0], 'to_dict'):
                    data[key] = [item.to_dict(seen_ids=seen_ids.copy()) for item in value]
                elif not value:
                    # Se la lista è vuota ma presente nel __dict__, 
                    # significa che la join è stata fatta ma non ci sono risultati.
                    data[key] = []

        return data
    def __repr__(self):
        """Rappresentazione leggibile per debug in console"""
        class_name = self.__class__.__name__
        obj_id = getattr(self, 'id', 'N/A')
        
        # Cerchiamo un campo descrittivo comune per rendere il log utile
        display_name = ""
        for field in ['name', 'contract_code', 'username', 'email']:
            if hasattr(self, field):
                val = getattr(self, field)
                display_name = f" {field}='{val}'"
                break
        
        return f"<{class_name} id={obj_id}{display_name}>"


# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import inspect

# db = SQLAlchemy()

# class BaseModel:
#     def to_dict(self, seen_ids=None):
#       if seen_ids is None:
#           seen_ids = set()
          
#       # Identificativo unico dell'oggetto per evitare cicli infiniti
#       obj_id = (self.__class__.__name__, self.id)
#       if obj_id in seen_ids:
#           return {"id": self.id} # Ritorna solo l'ID se lo abbiamo già processato
          
#       seen_ids.add(obj_id)
      
#       # 1. Colonne della tabella
#       data = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
      
#       # 2. Relazioni (Scende finché trova dati caricati)
#       for rel in inspect(self).mapper.relationships:
#           # Recuperiamo il valore (se il service ha fatto joinedload, è già qui)
#           value = getattr(self, rel.key)
          
#           if value is None:
#               data[rel.key] = None
#           elif hasattr(value, 'to_dict'):
#               # Relazione singola
#               data[rel.key] = value.to_dict(seen_ids=seen_ids.copy())
#           elif isinstance(value, (list, iter, any)): 
#               # Liste di oggetti (es. settori, contratti)
#               try:
#                   data[rel.key] = [item.to_dict(seen_ids=seen_ids.copy()) 
#                                   for item in value if hasattr(item, 'to_dict')]
#               except:
#                   # Se non è iterabile o genera errore (es. lazy loading non inizializzato)
#                   data[rel.key] = []
                  
#       return data
#     # def to_dict(self, depth=0):
#     #     # 1. Prendi le colonne semplici della tabella
#     #     data = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        
#     #     # 2. Se depth > 0, naviga nelle relazioni
#     #     if depth > 0:
#     #         for rel in inspect(self).mapper.relationships:
#     #             value = getattr(self, rel.key)
                
#     #             if value is None:
#     #                 data[rel.key] = None
#     #             elif hasattr(value, 'to_dict'):
#     #                 # Relazione singola (es. Contract.client)
#     #                 data[rel.key] = value.to_dict(depth=depth - 1)
#     #             else:
#     #                 # Relazione lista (es. GroupCompany.sectors)
#     #                 # Gestisce il caso delle liste di oggetti (Many-to-Many o One-to-Many)
#     #                 try:
#     #                     data[rel.key] = [item.to_dict(depth=depth - 1) for item in value]
#     #                 except TypeError:
#     #                     # Se non è iterabile (es. caricamento dinamico non inizializzato)
#     #                     data[rel.key] = []
        
#     #     return data
#     # def to_dict(self, nested=True):
#     #     # ... la logica che abbiamo scritto prima ...
#     #     return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

#     def __repr__(self):
#         """
#         Crea una rappresentazione leggibile automatica: <Modello id=123>
#         """
#         # Prende il nome della classe (es. Client, Contract)
#         class_name = self.__class__.__name__
#         # Prova a prendere l'ID se esiste
#         obj_id = getattr(self, 'id', 'N/A')
#         # Se c'è un campo 'name' o 'code', lo aggiungiamo per chiarezza
#         extra = ""
#         for field in ['name', 'contract_code', 'username']:
#             if hasattr(self, field):
#                 extra = f" {field}='{getattr(self, field)}'"
#                 break
        
#         return f"<{class_name} id={obj_id}{extra}>"