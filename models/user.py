from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, username, email, password_hash):
        self.username = username
        self.email = email
        self.password_hash = password_hash

    @classmethod
    def create(cls, username, email, password):
        password_hash = generate_password_hash(password)
        return cls(username, email, password_hash)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def from_document(cls, doc):
        """Crea una instancia de User a partir de un documento de MongoDB."""
        return cls(
            doc.get('username'),
            doc.get('email'),
            doc.get('password_hash')
        )

    # Puedes agregar aquí métodos para guardar y cargar usuarios desde la base de datos
